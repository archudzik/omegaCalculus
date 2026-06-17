from omega_calculus import OmegaContext, eval_rpn_generic, eval_rpn_pointwise, eval_rpn_trace, from_rpn, to_rpn, oslash, var


def test_rpn_generic():
    ctx = OmegaContext(2)
    assert eval_rpn_generic(["x1", "x2", "x2", "-", "oslash"], ctx) == ctx.x(1) * ctx.Omega


def test_rpn_roundtrip():
    expr = oslash(var(1), var(1))
    assert from_rpn(to_rpn(expr)) == expr


def test_rpn_pointwise_and_trace():
    ctx = OmegaContext(1)
    tokens = ["x1", "x1", "oslash"]
    assert eval_rpn_pointwise(tokens, {1: 0}, ctx) == 0
    assert eval_rpn_trace(tokens, {1: 0}, ctx).signature == (0,)
