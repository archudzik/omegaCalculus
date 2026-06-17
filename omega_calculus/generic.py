from __future__ import annotations

import sympy as sp

from .context import OmegaContext
from .expr import Add, Const, Expr, Mul, Omega, Oslash, Sub, Var, as_expr


def oslash_value(a: sp.Expr, b: sp.Expr, ctx: OmegaContext) -> sp.Expr:
    a = ctx.normalize(a)
    b = ctx.normalize(b)
    if ctx.is_zero(b):
        return ctx.normalize(a * ctx.Omega)
    return ctx.normalize(a / b)


def generic(expr: Expr, ctx: OmegaContext) -> sp.Expr:
    return ctx.normalize(_eval(as_expr(expr), ctx))


def _eval(expr: Expr, ctx: OmegaContext) -> sp.Expr:
    if isinstance(expr, Const):
        return ctx.normalize(expr.value)
    if isinstance(expr, Omega):
        return ctx.Omega
    if isinstance(expr, Var):
        return ctx.x(expr.index)
    if isinstance(expr, Add):
        return ctx.normalize(_eval(expr.left, ctx) + _eval(expr.right, ctx))
    if isinstance(expr, Sub):
        return ctx.normalize(_eval(expr.left, ctx) - _eval(expr.right, ctx))
    if isinstance(expr, Mul):
        return ctx.normalize(_eval(expr.left, ctx) * _eval(expr.right, ctx))
    if isinstance(expr, Oslash):
        return oslash_value(_eval(expr.left, ctx), _eval(expr.right, ctx), ctx)
    raise TypeError(f"unsupported expression: {expr!r}")
