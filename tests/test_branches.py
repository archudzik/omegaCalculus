from omega_calculus import OmegaContext, branch_stratification, oslash, var


def as_map(cells):
    return {cell.signature: cell for cell in cells}


def test_branch_stratification_two_divisions():
    ctx = OmegaContext(2)
    expr = oslash(1, var(1)) + oslash(1, var(2))
    cells = as_map(branch_stratification(expr, ctx))

    assert set(cells) == {(0, 0), (0, 1), (1, 0), (1, 1)}
    assert cells[(0, 0)].formula == 2 * ctx.Omega
    assert cells[(0, 1)].formula == ctx.normalize(ctx.Omega + 1 / ctx.x(2))
    assert cells[(1, 0)].formula == ctx.normalize(1 / ctx.x(1) + ctx.Omega)
    assert cells[(1, 1)].formula == ctx.normalize(1 / ctx.x(1) + 1 / ctx.x(2))

    assert cells[(0, 1)].equations == (ctx.x(1),)
    assert cells[(0, 1)].inequations == (ctx.x(2),)
