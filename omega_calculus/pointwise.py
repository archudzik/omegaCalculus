from __future__ import annotations

from typing import Any

import sympy as sp

from .context import OmegaContext
from .expr import Add, Const, Expr, Mul, Omega, Oslash, Sub, Var, as_expr
from .generic import oslash_value


def pointwise(expr: Expr, values: dict[Any, Any], ctx: OmegaContext) -> sp.Expr:
    return ctx.normalize(_eval(as_expr(expr), values, ctx))


def _eval(expr: Expr, values: dict[Any, Any], ctx: OmegaContext) -> sp.Expr:
    if isinstance(expr, Const):
        return ctx.normalize(expr.value)
    if isinstance(expr, Omega):
        return ctx.Omega
    if isinstance(expr, Var):
        return ctx.value_for_var(expr.index, values)
    if isinstance(expr, Add):
        return ctx.normalize(_eval(expr.left, values, ctx) + _eval(expr.right, values, ctx))
    if isinstance(expr, Sub):
        return ctx.normalize(_eval(expr.left, values, ctx) - _eval(expr.right, values, ctx))
    if isinstance(expr, Mul):
        return ctx.normalize(_eval(expr.left, values, ctx) * _eval(expr.right, values, ctx))
    if isinstance(expr, Oslash):
        return oslash_value(_eval(expr.left, values, ctx), _eval(expr.right, values, ctx), ctx)
    raise TypeError(f"unsupported expression: {expr!r}")
