from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp

from .context import OmegaContext
from .expr import Add, Const, Expr, Mul, Omega, Oslash, Sub, Var, as_expr
from .generic import oslash_value


@dataclass(frozen=True)
class TraceResult:
    value: sp.Expr
    signature: tuple[int, ...]


def trace(expr: Expr, values: dict[Any, Any], ctx: OmegaContext) -> TraceResult:
    result = _eval(as_expr(expr), values, ctx)
    return TraceResult(ctx.normalize(result.value), result.signature)


def _eval(expr: Expr, values: dict[Any, Any], ctx: OmegaContext) -> TraceResult:
    if isinstance(expr, Const):
        return TraceResult(ctx.normalize(expr.value), ())
    if isinstance(expr, Omega):
        return TraceResult(ctx.Omega, ())
    if isinstance(expr, Var):
        return TraceResult(ctx.value_for_var(expr.index, values), ())
    if isinstance(expr, Add):
        left = _eval(expr.left, values, ctx)
        right = _eval(expr.right, values, ctx)
        return TraceResult(ctx.normalize(left.value + right.value), left.signature + right.signature)
    if isinstance(expr, Sub):
        left = _eval(expr.left, values, ctx)
        right = _eval(expr.right, values, ctx)
        return TraceResult(ctx.normalize(left.value - right.value), left.signature + right.signature)
    if isinstance(expr, Mul):
        left = _eval(expr.left, values, ctx)
        right = _eval(expr.right, values, ctx)
        return TraceResult(ctx.normalize(left.value * right.value), left.signature + right.signature)
    if isinstance(expr, Oslash):
        left = _eval(expr.left, values, ctx)
        right = _eval(expr.right, values, ctx)
        bit = 0 if ctx.is_zero(right.value) else 1
        value = oslash_value(left.value, right.value, ctx)
        return TraceResult(value, left.signature + right.signature + (bit,))
    raise TypeError(f"unsupported expression: {expr!r}")
