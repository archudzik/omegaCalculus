import pytest

from omega_calculus import OmegaContext, generic, omega_degree, oslash, pointwise, trace, var


def repeated_oslash(value, divisor, count):
    expr = value
    for _ in range(count):
        expr = oslash(expr, divisor)
    return expr


def test_power_is_multiplication_sugar_not_branch_multiplicity():
    ctx = OmegaContext(1)
    r = var(1)
    expr = oslash(1200, r ** 6)

    assert generic(expr, ctx) == ctx.normalize(1200 / ctx.x(1) ** 6)
    assert pointwise(expr, {1: 0}, ctx) == 1200 * ctx.Omega
    assert trace(expr, {1: 0}, ctx).signature == (0,)
    assert omega_degree(pointwise(expr, {1: 0}, ctx), ctx) == 1


def test_repeated_oslash_counts_repeated_branch_events():
    ctx = OmegaContext(1)
    r = var(1)
    expr = repeated_oslash(1200, r, 6)

    assert pointwise(expr, {1: 0}, ctx) == 1200 * ctx.Omega ** 6
    assert trace(expr, {1: 0}, ctx).signature == (0, 0, 0, 0, 0, 0)
    assert omega_degree(pointwise(expr, {1: 0}, ctx), ctx) == 6


def test_power_zero_and_one():
    ctx = OmegaContext(1)
    r = var(1)

    assert generic(r ** 0, ctx) == 1
    assert generic(r ** 1, ctx) == ctx.x(1)


def test_negative_expression_power_rejected():
    with pytest.raises(ValueError):
        _ = var(1) ** -1
