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
    Categoricals are awesome!
    """

    def __init__(self, categories, value):
        # Categories are sorted unique lower case strings
        # Categoricals are integers refering to a category

        categories = {str(c).lower(): True for c in categories}
        categories = {c: k for k, c in enumerate(categories)}
        self._categories = categories

        if isinstance(value, int):
            if (value < 0) or (len(categories) <= value):
                raise ValueError
            self._value = value
        else:
            self._value = categories[str(value).lower()]

    def __int__(self):
        return self._value

    def __str__(self):
        w = self._value
        for c, v in self._categories.items():
            if v == w:
                return c

    def __repr__(self):
        return f"{type(self).__name__}[{', '.join(self._categories)}]({str(self)})"

    def __eq__(self, other):
        if isinstance(other, int):
            return int(self) == other
        return str(self) == str(other).lower()

    def categories(self):
        for c in self._categories:
            yield c


@TypeOrigin
class Multiple:
    """
    Multinominals are awesome, but hard to spell!
    """

    def __init__(self, categories, *values):
        # Categories are sorted unique lower case strings
        # Categoricals are sets of integers refering to a subset of the category
        categories = {str(c).lower(): True for c in categories}
        self._cat_key = {cat: key for key, cat in enumerate(categories)}
        self._key_cat = {key: cat for key, cat in enumerate(categories)}

        if all(isinstance(v, int) for v in values):
            self._keys = set()
            for v in values:
                if v < 0 or len(self._cat_key) <= v:
                    raise ValueError
                self._keys.add(v)
        else:
            values = (str(v).lower() for v in values)
            self._keys = set(self._cat_key[v] for v in values)

    def __str__(self):
        values = ", ".join(self.values())
        return f"{{{values}}}"

    def __repr__(self):
        name = type(self).__name__
        cats = ", ".join(self._cat_key)
        values = ", ".join(self.values())
        return f"{name}[{cats}]({values})"

    def __eq__(self, other):
        if all(isinstance(o, int) for o in other):
            return self._keys == set(other)
        return self._cat_keyues() == {str(o).lower() for o in other}

    def __contains__(self, item):
        if isinstance(item, int):
            return item in self._keys
        else:
            return str(item).lower() in self.values()

    def keys(self):
        yield from self._keys

    def values(self):
        for key in self._keys:
            yield self._key_cat[key]

    def items(self):
        for key in self._keys:
            yield key, self._key_cat[key]

    def categories(self):
        for c in self._cat_key:
            yield c


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

    M = Multiple["a", "b", "c"]

    print(M)
    print("c" in M(0, 1))
    print(repr(M(0, 1)))
    print(M("a"))
