# omega-calculus

Reference implementation for the paper
**Omega-Calculus: Normal Forms and Branch Semantics for Scale-Promoting Division**.

This package is a small executable model of the paper's algebraic and semantic
core. It is intended for reproducibility, examples, and regression tests, not as
a general-purpose computer algebra system.

## Implemented semantics

The package implements the total binary operation

```text
a oslash b = a / b   if b != 0
a oslash b = a Omega if b == 0
```

over rational functions in `Q(Omega, x1, ..., xn)`.

It includes:

- generic evaluation into rational-function normal forms;
- specialization-aware pointwise evaluation;
- trace semantics recording zero/nonzero branch events;
- guarded branch stratification;
- Omega-degree calculations;
- the zero-sensitive cancellation law;
- reverse Polish notation helpers.

## Scope

The implementation follows the paper's event-based semantics. Each occurrence
of `oslash` contributes at most one branch event. Powers of expression nodes are
expanded as repeated multiplication, not as repeated division events. Thus
`oslash(1200, r ** 6)` has one possible zero branch, while six successive calls to
`oslash(..., r)` have six possible zero branches.

Use `var(i)` and `omega()` to build syntax-sensitive expressions for pointwise
and trace semantics. Raw SymPy expressions are accepted as constants; they are
useful for generic algebra, but their internal symbols are not substituted by the
AST evaluator.

The package does not compute orders of vanishing, valuation refinements,
confluence for arbitrary rewrite systems, or bit-complexity bounds for symbolic
normalization.

## Quick example

```python
from omega_calculus import OmegaContext, generic, oslash, pointwise, trace, var

ctx = OmegaContext(n=1)
x1 = var(1)
T = oslash(x1, x1)

assert generic(T, ctx) == 1
assert pointwise(T, {1: 0}, ctx) == 0
assert trace(T, {1: 0}, ctx).signature == (0,)
```


## Powers and branch events

```python
from omega_calculus import OmegaContext, oslash, pointwise, trace, var

ctx = OmegaContext(n=1)
r = var(1)

expr = oslash(1200, r ** 6)
assert pointwise(expr, {1: 0}, ctx) == 1200 * ctx.Omega
assert trace(expr, {1: 0}, ctx).signature == (0,)

repeated = 1200
for _ in range(6):
    repeated = oslash(repeated, r)

assert pointwise(repeated, {1: 0}, ctx) == 1200 * ctx.Omega**6
assert trace(repeated, {1: 0}, ctx).signature == (0, 0, 0, 0, 0, 0)
```

## Install

From this directory:

```bash
python -m pip install -e .
```

For running the test suite:

```bash
python -m pip install -e ".[test]"
python -m pytest
```

The only runtime dependency is `sympy`.

## Repository layout

```text
omega_calculus/   package source
tests/            regression tests for the paper examples and laws
examples/         small usage scripts
pyproject.toml    install and test metadata
```

## Minimal usage

```python
from omega_calculus import OmegaContext, branch_stratification, oslash, var

ctx = OmegaContext(n=2)
x1 = var(1)
x2 = var(2)

expr = oslash(1, x1) + oslash(1, x2)
for cell in branch_stratification(expr, ctx):
    print(cell.signature, cell.equations, cell.inequations, cell.formula)
```

## Citation

If you use this model, please cite the accompanying paper and the Zenodo record
linked in the repository sidebar.
