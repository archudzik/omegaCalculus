from __future__ import annotations

from typing import Any, Iterable

import sympy as sp

from .context import OmegaContext
from .expr import Add, Const, Expr, Mul, Omega, Oslash, Sub, Var, as_expr, const, omega, oslash, var
from .generic import generic
from .pointwise import pointwise
from .trace import TraceResult, trace

OPERATORS = {"+", "-", "*", "·", "oslash", "⊘"}


def to_rpn(expr: Expr) -> list[Any]:
    expr = as_expr(expr)
    if isinstance(expr, Const):
        return [expr.value]
    if isinstance(expr, Omega):
        return ["Omega"]
    if isinstance(expr, Var):
        return [f"x{expr.index}"]
    if isinstance(expr, Add):
        return to_rpn(expr.left) + to_rpn(expr.right) + ["+"]
    if isinstance(expr, Sub):
        return to_rpn(expr.left) + to_rpn(expr.right) + ["-"]
    if isinstance(expr, Mul):
        return to_rpn(expr.left) + to_rpn(expr.right) + ["*"]
    if isinstance(expr, Oslash):
        return to_rpn(expr.left) + to_rpn(expr.right) + ["oslash"]
    raise TypeError(f"unsupported expression: {expr!r}")


def from_rpn(tokens: Iterable[Any]) -> Expr:
    stack: list[Expr] = []
    for token in tokens:
        if token in {"+", "-", "*", "·", "oslash", "⊘"}:
            if len(stack) < 2:
                raise ValueError(f"operator {token!r} underflows the stack")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(Add(a, b))
            elif token == "-":
                stack.append(Sub(a, b))
            elif token in {"*", "·"}:
                stack.append(Mul(a, b))
            else:
                stack.append(Oslash(a, b))
        else:
            stack.append(_atom(token))
    if len(stack) != 1:
        raise ValueError(f"invalid RPN expression leaves {len(stack)} stack entries")
    return stack[0]


def eval_rpn_generic(tokens: Iterable[Any], ctx: OmegaContext) -> sp.Expr:
    return generic(from_rpn(tokens), ctx)


def eval_rpn_pointwise(tokens: Iterable[Any], values: dict[Any, Any], ctx: OmegaContext) -> sp.Expr:
    return pointwise(from_rpn(tokens), values, ctx)


def eval_rpn_trace(tokens: Iterable[Any], values: dict[Any, Any], ctx: OmegaContext) -> TraceResult:
    return trace(from_rpn(tokens), values, ctx)


def _atom(token: Any) -> Expr:
    if isinstance(token, Expr):
        return token
    if token == "Omega" or token == "Ω":
        return omega()
    if isinstance(token, str) and token.startswith("x") and token[1:].isdigit():
        return var(int(token[1:]))
    return const(sp.sympify(token))
