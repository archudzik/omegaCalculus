from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class OmegaContext:
    n: int
    omega_name: str = "Omega"
    variable_prefix: str = "x"

    def __post_init__(self) -> None:
        if self.n < 0:
            raise ValueError("n must be nonnegative")
        object.__setattr__(self, "Omega", sp.Symbol(self.omega_name))
        variables = tuple(sp.Symbol(f"{self.variable_prefix}{i}") for i in range(1, self.n + 1))
        object.__setattr__(self, "variables", variables)

    def x(self, index: int) -> sp.Symbol:
        if index < 1 or index > self.n:
            raise IndexError(f"variable index {index} is outside 1..{self.n}")
        return self.variables[index - 1]

    def normalize(self, value: Any) -> sp.Expr:
        return sp.cancel(sp.sympify(value))

    def is_zero(self, value: Any) -> bool:
        return self.normalize(value) == 0

    def fraction(self, value: Any) -> tuple[sp.Expr, sp.Expr]:
        value = self.normalize(value)
        numerator, denominator = sp.fraction(value)
        return self.normalize(numerator), self.normalize(denominator)

    def value_for_var(self, index: int, values: dict[Any, Any]) -> sp.Expr:
        symbol = self.x(index)
        keys = (index, symbol, str(symbol), f"x{index}")
        for key in keys:
            if key in values:
                return self.normalize(values[key])
        raise KeyError(f"missing value for {symbol}")
