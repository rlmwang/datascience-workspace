from .api.endpoint import route
from .api.typing import Categorical


@route
def predict(
    formula: Categorical["addition", "multiplication"],
    x: float,
    y: int,
) -> str:
    print(formula, x, y)
    if formula == "addition":
        return x + y
    elif formula == "multiplication":
        return x * y
    else:
        return x ** y


if __name__ == "__main__":
    pass
