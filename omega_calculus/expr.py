from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp


class Expr:
    def __add__(self, other: Any) -> Expr:
        return Add(self, as_expr(other))

    def __radd__(self, other: Any) -> Expr:
        return Add(as_expr(other), self)

    def __sub__(self, other: Any) -> Expr:
        return Sub(self, as_expr(other))

    def __rsub__(self, other: Any) -> Expr:
        return Sub(as_expr(other), self)

    def __mul__(self, other: Any) -> Expr:
        return Mul(self, as_expr(other))

    def __rmul__(self, other: Any) -> Expr:
        return Mul(as_expr(other), self)

    def __pow__(self, exponent: int) -> Expr:
        return pow_expr(self, exponent)

    def oslash(self, other: Any) -> Expr:
        return Oslash(self, as_expr(other))


@dataclass(frozen=True)
class Const(Expr):
    value: sp.Expr


@dataclass(frozen=True)
class Var(Expr):
    index: int


@dataclass(frozen=True)
class Omega(Expr):
    pass


@dataclass(frozen=True)
class Add(Expr):
    left: Expr
    right: Expr


@dataclass(frozen=True)
class Sub(Expr):
    left: Expr
    right: Expr


@dataclass(frozen=True)
class Mul(Expr):
    left: Expr
    right: Expr


@dataclass(frozen=True)
class Oslash(Expr):
    left: Expr
    right: Expr


def const(value: Any) -> Const:
    return Const(sp.sympify(value))


def var(index: int) -> Var:
    return Var(index)


def omega() -> Omega:
    return Omega()


def oslash(left: Any, right: Any) -> Oslash:
    return Oslash(as_expr(left), as_expr(right))


def as_expr(value: Any) -> Expr:
    if isinstance(value, Expr):
        return value
    return const(value)


def pow_expr(base: Any, exponent: int) -> Expr:
    if isinstance(exponent, bool) or not isinstance(exponent, int):
        raise TypeError("expression powers require a nonnegative integer exponent")
    if exponent < 0:
        raise ValueError(
            "negative expression powers are not part of the core syntax; "
            "use oslash(1, expr ** k) for reciprocal powers"
        )

    base_expr = as_expr(base)
    if exponent == 0:
        return const(1)

    result = base_expr
    for _ in range(exponent - 1):
        result = Mul(result, base_expr)
    return result
