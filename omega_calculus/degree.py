from __future__ import annotations

from math import inf
from typing import Any

import sympy as sp

from .context import OmegaContext
from .expr import Expr
from .generic import generic

NEG_INF = -inf


def omega_degree(value: Any, ctx: OmegaContext) -> int | float:
    if isinstance(value, Expr):
        value = generic(value, ctx)
    value = ctx.normalize(value)
    if value == 0:
        return NEG_INF
    numerator, denominator = ctx.fraction(value)
    return int(sp.degree(numerator, ctx.Omega) - sp.degree(denominator, ctx.Omega))
