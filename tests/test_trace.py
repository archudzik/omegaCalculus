from omega_calculus import OmegaContext, oslash, trace, var


def test_trace_records_branch_signature():
    ctx = OmegaContext(2)
    expr = oslash(1, var(1)) + oslash(1, var(2))
    result = trace(expr, {1: 0, 2: 3}, ctx)
    assert result.signature == (0, 1)
    assert result.value == ctx.normalize(ctx.Omega + ctx.normalize("1/3"))


def test_same_value_can_have_different_histories():
    ctx = OmegaContext(1)
    zero_branch = trace(oslash(2, 0), {}, ctx)
    nonzero_branch = trace(oslash(2 * ctx.Omega, 1), {}, ctx)
    assert zero_branch.value == nonzero_branch.value
    assert zero_branch.signature != nonzero_branch.signature
