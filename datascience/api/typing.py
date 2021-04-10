"""
Extends the typing module with some useful types for data science.
"""
import datetime as dt
from typing import NewType
from typing import get_args as tp_get_args
from typing import get_origin as tp_get_origin

File = NewType("File", str)
Image = NewType("Image", str)
Audio = NewType("Audio", str)
Video = NewType("Video", str)

Url = NewType("Url", str)
Email = NewType("Email", str)


"""
Extend get_origin and get_args
"""


def get_origin(tp):
    return tp_get_origin(tp) or (tp.__origin__ if type(tp) is TypeAlias else None)


def get_args(tp):
    return tp_get_args(tp) or (tp.__args__ if type(tp) is TypeAlias else ())


"""
Categorical, Multiple (multinominal)
And trickery from a typing module
"""


class TypeAlias:
    def __init__(self, origin, args):
        self.__origin__ = origin
        self.__args__ = args

        _name = origin.__name__
        _args = (str(a) for a in args)
        self.__name__ = f"{_name}[{', '.join(_args)}]"

    def __repr__(self):
        return self.__name__

    def __call__(self, *args, **kwargs):
        return self.__origin__(self.__args__, *args, **kwargs)


class TypeOrigin:
    def __init__(self, cls):
        self.__name__ = cls.__name__
        self.__doc__ = cls.__doc__
        self._type = cls

    def __repr__(self):
        return self.__name__

    def __getitem__(self, args):
        return TypeAlias(self, args)

    def __call__(self, *args, **kwargs):
        return self._type(*args, **kwargs)


@TypeOrigin
class Categorical:
    """
    Categorical is awesome!
    """

    def __init__(self, categories, value):
        self.categories = {str(c): True for c in categories}
        assert str(value) in categories


@TypeOrigin
class Multiple(set[str]):
    """
    Multinominals are awesome, but hard to spell!
    """

    def __post_init__(self, categories, *values):
        categories = {str(c): True for c in categories}
        values = set(str(v) for v in values)

        assert all(v in categories for v in values)
        self._categories = categories

        super().__init__(values)


"""
Dictionaries
"""


classes = {
    "audio": Audio,
    "bool": bool,
    "categorical": Categorical,
    "date": dt.datetime,
    "datetime": dt.datetime,
    "email": Email,
    "file": File,
    "float": float,
    "image": Image,
    "int": int,
    "multiple": Multiple,
    "str": str,
    "url": Url,
    "video": Video,
}


if __name__ == "__main__":
    from inspect import signature

    print(Categorical.__doc__)

    X = Categorical[1, 2]
    Orig = get_origin(X)

    assert isinstance(X, TypeAlias)
    assert X.__name__ == "Categorical[1, 2]"
    assert isinstance(Orig, TypeOrigin)
    assert Orig.__name__ == "Categorical"
    assert get_args(X) == (1, 2)

    A = Categorical[1, 2]
    B = Categorical[2, 1]
    assert A != B

    a = Categorical[1, 2](1)
    b = Categorical[2, 1](1)
    c = Categorical((1, 2), 1)
    assert a == b
    assert a == c

    def f(x: Categorical["a", "b"], y: File) -> None:
        pass

    print(f"{signature(f)}\n")

    X = Categorical["b", "a"]
    print(X)
    print(f"Origin: {get_origin(X)}")
    print(f"Arguments: {get_args(X)}\n")
