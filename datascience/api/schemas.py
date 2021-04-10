"""
Builds inputs and output schemas from a function.
"""
from pathlib import Path
from typing import Any, Callable

from marshmallow import Schema
from marshmallow import fields as fd

from . import config
from .inspect import inspect_inputs, inspect_output


def get_inputs_schema(func: Callable[..., Any]) -> tuple[dict, Schema]:
    dschema = getattr(func, "inputs_schema", None)
    dschema = dschema or inspect_inputs(func)

    return (
        dschema,
        Schema.from_dict(
            {field: build_field(meta["dtype"]) for field, meta in dschema.items()}
        )(),
    )


def get_output_schema(func: Callable[..., Any]) -> tuple[dict, Schema]:
    dschema = getattr(func, "output_schema", None)
    dschema = dschema or inspect_output(func)

    return (
        dschema,
        Schema.from_dict(
            {field: build_field(meta["dtype"]) for field, meta in dschema.items()}
        )(),
    )


def build_field(dtype):
    field = FIELDS.get(dtype["name"], FIELDS["default"])
    return field(*dtype["args"])


"""
Schemas
"""

default_error_messages = {
    "invalid": "Not a valid file.",
}

inputs_dir = config.INPUTS_FOLDER
output_dir = config.OUTPUT_FOLDER


class File(fd.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return Path(inputs_dir, value).as_posix()

    def _deserialize(self, value, attr, data, **kwargs):
        return Path(output_dir, Path(value).name).as_posix()


class Image(fd.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return Path(inputs_dir, value).as_posix()

    def _deserialize(self, value, attr, data, **kwargs):
        return Path(output_dir, Path(value).name).as_posix()


class Audio(fd.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return Path(inputs_dir, value).as_posix()

    def _deserialize(self, value, attr, data, **kwargs):
        return Path(output_dir, Path(value).name).as_posix()


class Video(fd.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return Path(inputs_dir, value).as_posix()

    def _deserialize(self, value, attr, data, **kwargs):
        return Path(output_dir, Path(value).name).as_posix()


class Categorical(fd.Field):
    def __init__(self, *args):
        super().__init__()
        self.categories = args

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value


class Multiple(fd.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value


"""
Dictionaries
"""

FIELDS = {
    "audio": Audio,
    "bool": fd.Boolean,
    "categorical": Categorical,
    "date": fd.Date,
    "datetime": fd.DateTime,
    "default": fd.String,
    "email": fd.Email,
    "file": File,
    "image": Image,
    "int": fd.Integer,
    "float": fd.Float,
    "multiple": Multiple,
    "str": fd.String,
    "url": fd.Url,
    "video": Video,
}
