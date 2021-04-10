import os
from typing import Any, Callable, TypeVar, overload

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from . import config
from .schemas import get_inputs_schema, get_output_schema

blueprints: list[Blueprint] = []


F = TypeVar("F", bound=Callable[..., Any])


def inputs(func, schema=None):
    if schema is not None:
        func.inputs_schema = schema
    else:

        def decorator(schema):
            func.inputs_schema = schema
            return schema

        return decorator


def output(func, schema=None):
    if schema is not None:
        func.output_schema = schema
    else:

        def decorator(schema):
            func.output_schema = schema
            return schema

        return decorator


# fmt: off
@overload
def route(func_endpoint: F) -> F: ...
@overload
def route(func_endpoint: str) -> Callable[[F], F]: ...
# fmt: on


def route(func_endpoint):
    """
    The route to success!
    """

    def decorator(func: F) -> F:

        if isinstance(func_endpoint, str):
            endpoint = func_endpoint
        else:
            endpoint = "/" + func.__name__

        blue = Blueprint(endpoint, __name__)
        blueprints.append(blue)

        @blue.route(endpoint, methods=["GET", "POST"])
        def _route():
            idict, ischema = get_inputs_schema(func)
            odict, oschema = get_output_schema(func)

            if request.method == "GET":
                return render(request, idict, odict)

            if request.is_json:
                is_backend = True
                inputs = request.get_json()
            else:
                is_backend = False

                inputs = request.form
                files = request.files
                url = request.url

                inputs = process_frontend(idict, inputs, files, url)

            print("\n", inputs, "\n")

            inputs = process_inputs(ischema, inputs)
            output = func(**inputs)
            output = process_output(oschema, output)

            if is_backend:
                return output

            idict = merge_schema_values(idict, inputs)
            odict = merge_schema_values(odict, output)

            print("\n", idict, "\n", odict, "\n")

            return render(request, idict, odict)

        return func

    if isinstance(func_endpoint, str):
        return decorator
    else:
        return decorator(func_endpoint)


def process_inputs(ischema, values):
    return ischema.load(values)


def process_output(oschema, values):
    if not isinstance(values, tuple):
        values = (values,)
    return oschema.dump({field: value for field, value in zip(oschema.fields, values)})


def merge_schema_values(schema, values):
    return {field: schema[field] | {"value": values[field]} for field in schema}


def process_frontend(ischema, inputs, files, url):
    """
    Handle any processing necessary to align the input from
    the frontend with the expected input at the backend.
    """
    for name, meta in ischema.items():
        dtype = meta["dtype"]

        if dtype in ("file", "image", "audio", "video"):
            inputs[name] = process_file(name, files, url)

    return inputs


def process_file(name, files, url):
    """
    Save file to shared folder on server, and return
    the name of the file.
    """

    def allowed_file(filename):
        if "." not in filename:
            return False
        ext = filename.rsplit(".", 1)[1].lower()
        return ext in config.ALLOWED_EXTENSIONS

    if name not in files:
        flash("No file part found")
        return redirect(url)

    file = files[name]

    if not file.filename:
        flash("No file selected")
        return redirect(url)

    if not allowed_file(file.filename):
        flash("File is not allowed")
        return redirect(url)

    filename = secure_filename(file.filename)
    filepath = os.path.join(config.INPUTS_FOLDER, filename)

    file.save(filepath)
    return filename


def render(request, ischema, oschema):
    return render_template(
        "index.html",
        inputs=[
            {
                "name": field,
                "value": meta["value"],
                "dtype": meta["dtype"],
                "default": meta["default"],
            }
            for field, meta in ischema.items()
        ],
        output=[
            {
                "name": field,
                "value": meta["value"],
                "dtype": meta["dtype"],
                "default": meta["default"],
            }
            for field, meta in oschema.items()
        ],
        sitemap=sitemap(request),
    )


def sitemap(request):

    rules = []
    current = request.url_rule.rule

    for rule in config.app.url_map.iter_rules():
        if "GET" not in rule.methods:
            continue
        if has_empty_params(rule):
            continue

        url = url_for(rule.endpoint, **(rule.defaults or {}))

        rules.append(
            {
                "url": url,
                "name": url.strip("/") or "home",
                "active": rule.rule == current,
            }
        )

    return rules


def has_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) < len(arguments)
