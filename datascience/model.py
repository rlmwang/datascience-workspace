from .api.endpoint import route
from .api.typing import Categorical, Multiple


@route
def predict(
    x: float,
    y: int,
    formula: Multiple["addition", "multiplication"] = None,
) -> str:
    """
    Frickin' [sic]
    """
    res = []
    if "addition" in formula:
        res.append(x + y)
    if "multiplication" in formula:
        res.append(x * y)
    return res


if __name__ == "__main__":
    pass
