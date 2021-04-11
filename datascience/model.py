from .api.endpoint import route
from .api.typing import Categorical


@route
def predict(
    x: float,
    y: int = None,
    formula: Categorical["addition", "multiplication"] = None,
) -> str:
    if formula == "addition":
        return x + y
    elif formula == "multiplication":
        return x * y
    else:
        return x ** y


if __name__ == "__main__":
    pass
