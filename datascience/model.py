from .api.endpoint import route
from .api.typing import Categorical, Multiple


@route
def predict(
    foo: bool,
    x: float,
    y: int,
    formula: Multiple["addition", "multiplication"] = None,
) -> str:

    """
    Frickin' [sic]
    """

    if foo:
        return 9000

    res = []
    if "addition" in formula:
        res.append(x + y)
    if "multiplication" in formula:
        res.append(x * y)
    return res


if __name__ == "__main__":
    pass
