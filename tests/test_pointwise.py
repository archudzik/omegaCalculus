from omega_calculus import OmegaContext, generic, oslash, pointwise, var


def test_generic_and_pointwise_differ_on_branch_locus():
    ctx = OmegaContext(1)
    x1 = var(1)
    expr = oslash(x1, x1)
    assert generic(expr, ctx) == 1
    assert pointwise(expr, {1: 0}, ctx) == 0
    assert pointwise(expr, {1: 2}, ctx) == 1


def test_pointwise_activates_zero_branch():
    ctx = OmegaContext(1)
    expr = oslash(1, var(1))
    assert pointwise(expr, {1: 0}, ctx) == ctx.Omega
    assert pointwise(expr, {1: 4}, ctx) == ctx.normalize("1/4")


def test_cancellation_trap_generic_zero_special_scale():
    ctx = OmegaContext(1)
    x1 = var(1)
    expr = oslash(oslash(x1, x1) - 1, oslash(x1, x1))

    assert generic(expr, ctx) == 0
    assert pointwise(expr, {1: 0}, ctx) == -ctx.Omega
    assert pointwise(expr, {1: 2}, ctx) == 0
