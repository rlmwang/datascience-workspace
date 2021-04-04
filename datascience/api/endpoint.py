import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename

from ..marshmallow import Categorical
from . import config

blueprints: list[Blueprint] = []
ischemas: dict[str, Schema] = {}
oschemas: dict[str, Schema] = {}


def decorator(deco):
    def wrapper(*args, **kwargs):
        def _deco(func):
            return deco(func, *args, **kwargs)

        return _deco

    return wrapper


@decorator
def inputs(schema, endpoint):
    ischemas[endpoint] = schema()
    return schema


@decorator
def output(schema, endpoint):
    oschemas[endpoint] = schema()
    return schema


@decorator
def endpoint(predict, endpoint, itype, otype):

    blue = Blueprint(endpoint, __name__)
    blueprints.append(blue)

    @blue.route(endpoint, methods=["GET", "POST"])
    def _endpoint():
        if request.method == "GET":
            return render(endpoint, itype, otype)

        inputs, backend = process_request(endpoint, itype)
        inputs = process_inputs(endpoint, itype, inputs)
        output = predict(**inputs)
        output = process_output(endpoint, output)

        if backend:
            return output

        if otype == "audio":
            output["result"] = os.path.join(config.OUTPUT_FOLDER, output["result"])

        return render(endpoint, itype, otype, inputs=inputs, output=output)

    return predict


def process_request(endpoint, itype):
    if request.is_json:
        inputs = request.get_json()
        return inputs, True

    # Web GUI input processing
    # Standardize like the back-end
    inputs = request.form  # .to_dict(flat=False)

    if itype == "image":
        filename = process_image_request()
        inputs["image"] = filename
    if itype == "audio":
        filename = process_audio_request()
        inputs["audio"] = filename

    return inputs, False


def process_image_request():
    return process_file_request("image")


def process_audio_request():
    return process_file_request("audio")


def process_file_request(field):

    if field not in request.files:
        flash("No file part found")
        return redirect(request.url)

    file = request.files[field]

    if file.filename == "":
        flash("No file selected")
        return redirect(request.url)

    if not allowed_file(file.filename):
        flash("File is not allowed")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    filepath = os.path.join(config.INPUTS_FOLDER, filename)

    file.save(filepath)

    return filename


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )


def process_inputs(endpoint, itype, inputs):
    ischema = ischemas.get(endpoint, None)

    if ischema is not None:
        inputs = ischema.load(inputs)

    if itype == "image":
        inputs["image"] = os.path.join(config.INPUTS_FOLDER, inputs["image"])
    elif itype == "audio":
        inputs["audio"] = os.path.join(config.INPUTS_FOLDER, inputs["audio"])

    return inputs


def process_output(endpoint, output):
    oschema = oschemas.get(endpoint, None)
    if oschema is not None:
        output = oschema.dump(
            {
                "result": output,
                "version": "0.0.1",
            }
        )
    return output


def field_to_dtype(field):
    if isinstance(field, fields.Boolean):
        return "boolean"
    elif isinstance(field, fields.Number):
        return "number"
    elif isinstance(field, Categorical):
        return "categorical"
    else:
        return "other"


def render(endpoint, itype, otype, inputs={}, output={}):
    ischema = ischemas.get(endpoint, {})
    oschema = oschemas.get(endpoint, {})

    return render_template(
        "base.html",
        inputs_template=f"inputs/{itype}.html",
        output_template=f"output/{otype}.html",
        inputs=[
            {
                "name": item,
                "dtype": field_to_dtype(field),
                "value": inputs.get(item, field.missing),
            }
            for item, field in ischema.fields.items()
        ],
        output=[
            {"name": item, "value": output.get(item, field.default)}
            for item, field in oschema.fields.items()
        ],
        sitemap=sitemap(),
    )


blue = Blueprint("/sitemap", __name__)
blueprints.append(blue)


@blue.route("/sitemap", methods=["GET"])
def sitemap():
    rules = []

    current = request.url_rule.rule

    for rule in config.app.url_map.iter_rules():
        if "GET" not in rule.methods:
            continue
        if not has_no_empty_params(rule):
            continue

        url = url_for(rule.endpoint, **(rule.defaults or {}))

        if url == "/sitemap":
            continue

        active = "mdc-list-item--activated" if rule.rule in current else ""

        rules.append((url, active))

    return render_template("sitemap.html", rules=rules)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
