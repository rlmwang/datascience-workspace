import enum
from typing import Literal, Union


class LinkageCriterion(enum.Enum):
    WARD = "ward"
    COMPLETE = "complete"
    AVERAGE = "average"
    SINGLE = "single"


LinkageCriterionLike = Union[
    LinkageCriterion,
    Literal[tuple(x.value for x in LinkageCriterion)],
]

if __name__ == "__main__":
    print(LinkageCriterionLike)
