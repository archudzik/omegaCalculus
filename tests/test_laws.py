from omega_calculus import OmegaContext, chi, oslash_value, zero_sensitive_cancellation


def test_chi_values_and_idempotence():
    ctx = OmegaContext(1)
    x1 = ctx.x(1)
    assert chi(0, ctx) == 0
    assert chi(x1, ctx) == 1
    assert ctx.normalize(chi(x1, ctx) ** 2 - chi(x1, ctx)) == 0


def test_zero_sensitive_cancellation_cases():
    ctx = OmegaContext(1)
    a = ctx.x(1) + 2
    for b in [0, ctx.x(1), ctx.Omega + 1]:
        left, right = zero_sensitive_cancellation(a, b, ctx)
        assert ctx.normalize(left - right) == 0


def test_non_identifiability_of_zero_branch():
    ctx = OmegaContext(1)
    y = ctx.x(1) + ctx.Omega
    assert oslash_value(y * ctx.Omega**-1, 0, ctx) == oslash_value(y, 1, ctx)
