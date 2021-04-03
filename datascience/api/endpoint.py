import os

from flask import Blueprint, flash, redirect, render_template, request
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename

from . import config
from .utils import field_to_html

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

    blueprint = Blueprint(endpoint, __name__)
    blueprints.append(blueprint)

    @blueprint.route(endpoint, methods=["GET", "POST"])
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
                "html": field_to_html(field, item),
                "value": inputs.get(item, field.missing),
            }
            for item, field in ischema.fields.items()
        ],
        output=[
            {"name": item, "value": output.get(item, field.default)}
            for item, field in oschema.fields.items()
        ],
    )
