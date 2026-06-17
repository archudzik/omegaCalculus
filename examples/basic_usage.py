from omega_calculus import OmegaContext, branch_stratification, generic, oslash, pointwise, trace, var

ctx = OmegaContext(n=2)
x1 = var(1)
x2 = var(2)

T = oslash(x1, x1)
print("generic:", generic(T, ctx))
print("pointwise x1=0:", pointwise(T, {1: 0}, ctx))
print("trace x1=0:", trace(T, {1: 0}, ctx))

U = oslash(1, x1) + oslash(1, x2)
for cell in branch_stratification(U, ctx):
    print(cell)
