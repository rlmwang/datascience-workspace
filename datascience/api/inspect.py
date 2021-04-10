import re
from inspect import Parameter, signature

from .typing import get_args, get_origin


def inspect_inputs(func):
    """
    Inspects the signature of a function and returns its
    input parameters as a dictionary.
    """
    parameters = signature(func).parameters

    return {
        param.name: {
            "dtype": get_type(param.annotation),
            "value": None,
            "default": get_default(param),
        }
        for param in parameters.values()
    }


def inspect_output(func):
    """
    Inspects the signature of a function and returns its
    output parameters as a dictionary.
    """
    anno = signature(func).return_annotation
    name = getattr(anno, "__name__", None)

    if name == "tuple":
        args = get_args(anno)
    else:
        args = (anno,)

    return {
        f"output {k:02d}": {
            "dtype": get_type(arg),
            "value": None,
            "default": None,
        }
        for k, arg in enumerate(args)
    }


def get_default(param):
    d = getattr(param, "default", None)
    d = None if d is Parameter.empty else d
    return d


def get_type(anno):

    origin = get_origin(anno)
    if origin is not None:
        return {
            "name": to_camel_case(getattr(origin, "__name__", None)),
            "args": tuple(get_type(a) for a in get_args(anno)),
        }

    name = to_camel_case(getattr(anno, "__name__", None))
    name = None if name == "_empty" else str(anno) if name is None else name

    if name == "ndarray":
        return {
            "name": "ndarray",
            "args": tuple(anno.dtype.name),
        }

    return {
        "name": name,
        "args": (),
    }


def to_camel_case(string):
    if string is None:
        return None
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return re.sub(pattern, "_", string).lower()
