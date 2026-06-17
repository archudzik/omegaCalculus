from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp

from .context import OmegaContext
from .expr import Expr
from .rpn import from_rpn, to_rpn


@dataclass(frozen=True)
class FractionState:
    numerator: sp.Expr
    denominator: sp.Expr

    def expr(self, ctx: OmegaContext) -> sp.Expr:
        return ctx.normalize(self.numerator / self.denominator)


@dataclass(frozen=True)
class BranchCell:
    signature: tuple[int, ...]
    equations: tuple[sp.Expr, ...]
    inequations: tuple[sp.Expr, ...]
    formula: sp.Expr


@dataclass(frozen=True)
class _State:
    signature: tuple[int, ...]
    equations: tuple[sp.Expr, ...]
    inequations: tuple[sp.Expr, ...]
    stack: tuple[FractionState, ...]


def branch_stratification(expr: Expr, ctx: OmegaContext) -> list[BranchCell]:
    states = [_State((), (), (), ())]
    for token in to_rpn(expr):
        states = _step(states, token, ctx)
    cells: list[BranchCell] = []
    for state in states:
        if len(state.stack) != 1:
            raise ValueError("invalid expression leaves a non-singleton stack")
        cells.append(
            BranchCell(
                signature=state.signature,
                equations=state.equations,
                inequations=state.inequations,
                formula=state.stack[0].expr(ctx),
            )
        )
    return cells


def _step(states: list[_State], token: Any, ctx: OmegaContext) -> list[_State]:
    if token == "+":
        return [_binary(state, ctx, lambda a, b: _add(a, b, ctx)) for state in states]
    if token == "-":
        return [_binary(state, ctx, lambda a, b: _sub(a, b, ctx)) for state in states]
    if token == "*":
        return [_binary(state, ctx, lambda a, b: _mul(a, b, ctx)) for state in states]
    if token == "oslash":
        new_states: list[_State] = []
        for state in states:
            if len(state.stack) < 2:
                raise ValueError("oslash underflows the stack")
            b = state.stack[-1]
            a = state.stack[-2]
            rest = state.stack[:-2]
            r = ctx.normalize(b.numerator)
            zero_value = _normalize_fraction(a.numerator * ctx.Omega, a.denominator, ctx)
            nonzero_value = _normalize_fraction(a.numerator * b.denominator, a.denominator * b.numerator, ctx)
            new_states.append(
                _State(
                    state.signature + (0,),
                    state.equations + (r,),
                    state.inequations,
                    rest + (zero_value,),
                )
            )
            new_states.append(
                _State(
                    state.signature + (1,),
                    state.equations,
                    state.inequations + (r,),
                    rest + (nonzero_value,),
                )
            )
        return new_states
    return [_push_atom(state, token, ctx) for state in states]


def _push_atom(state: _State, token: Any, ctx: OmegaContext) -> _State:
    expr = from_rpn([token])
    from .generic import generic

    value = generic(expr, ctx)
    numerator, denominator = ctx.fraction(value)
    return _State(state.signature, state.equations, state.inequations, state.stack + (FractionState(numerator, denominator),))


def _binary(state: _State, ctx: OmegaContext, op) -> _State:
    if len(state.stack) < 2:
        raise ValueError("binary operator underflows the stack")
    b = state.stack[-1]
    a = state.stack[-2]
    return _State(state.signature, state.equations, state.inequations, state.stack[:-2] + (op(a, b),))


def _add(a: FractionState, b: FractionState, ctx: OmegaContext) -> FractionState:
    return _normalize_fraction(a.numerator * b.denominator + b.numerator * a.denominator, a.denominator * b.denominator, ctx)


def _sub(a: FractionState, b: FractionState, ctx: OmegaContext) -> FractionState:
    return _normalize_fraction(a.numerator * b.denominator - b.numerator * a.denominator, a.denominator * b.denominator, ctx)


def _mul(a: FractionState, b: FractionState, ctx: OmegaContext) -> FractionState:
    return _normalize_fraction(a.numerator * b.numerator, a.denominator * b.denominator, ctx)


def _normalize_fraction(numerator: Any, denominator: Any, ctx: OmegaContext) -> FractionState:
    value = ctx.normalize(sp.sympify(numerator) / sp.sympify(denominator))
    p, q = ctx.fraction(value)
    return FractionState(p, q)
