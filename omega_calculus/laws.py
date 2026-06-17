from __future__ import annotations

from typing import Any

import sympy as sp

from .context import OmegaContext
from .generic import oslash_value


def chi(b: Any, ctx: OmegaContext) -> sp.Expr:
    b = ctx.normalize(b)
    return oslash_value(b, b, ctx)


def zero_sensitive_cancellation(a: Any, b: Any, ctx: OmegaContext) -> tuple[sp.Expr, sp.Expr]:
    a = ctx.normalize(a)
    b = ctx.normalize(b)
    left = ctx.normalize(oslash_value(a, b, ctx) * b)
    right = ctx.normalize(a * chi(b, ctx))
    return left, right
