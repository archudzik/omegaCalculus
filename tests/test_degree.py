from math import isinf

from omega_calculus import OmegaContext, omega_degree, oslash, var


def test_omega_degree_values():
    ctx = OmegaContext(2)
    O = ctx.Omega
    x1 = ctx.x(1)
    assert omega_degree(0, ctx) == float("-inf")
    assert omega_degree(5, ctx) == 0
    assert omega_degree(x1 + 3, ctx) == 0
    assert omega_degree(O, ctx) == 1
    assert omega_degree(1 / O, ctx) == -1
    assert omega_degree(O**2 + x1, ctx) == 2
    assert omega_degree((x1 + 1) / O, ctx) == -1


def test_scale_degree_promotion():
    ctx = OmegaContext(1)
    O = ctx.Omega
    f = (O**2 + 1) / (O - 3)
    assert omega_degree(f, ctx) == 1
    assert omega_degree(oslash(f, 0), ctx) == 2
