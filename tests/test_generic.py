import sympy as sp

from omega_calculus import OmegaContext, generic, omega, oslash, var


def test_basic_zero_branch():
    ctx = OmegaContext(2)
    assert generic(oslash(1, 0), ctx) == ctx.Omega
    assert generic(oslash(0, 0), ctx) == 0
    assert generic(oslash(2, 0), ctx) == 2 * ctx.Omega
    assert generic(oslash(-1, 0), ctx) == -ctx.Omega


def test_formal_variables_generic_semantics():
    ctx = OmegaContext(2)
    x1 = var(1)
    x2 = var(2)
    assert generic(oslash(x1, x2), ctx) == ctx.x(1) / ctx.x(2)
    assert generic(oslash(x1, x2 - x2), ctx) == ctx.x(1) * ctx.Omega


def test_no_inverse_of_zero_claim_needed():
    ctx = OmegaContext(1)
    assert generic(oslash(1, 0) * 0, ctx) == 0
