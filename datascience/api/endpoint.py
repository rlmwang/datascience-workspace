import os

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
)
from marshmallow import Schema
from werkzeug.utils import secure_filename

from . import config
from .utils import field_to_html

blueprints: list[Blueprint] = []
inputs_schemas: dict[str, Schema] = {}
output_schemas: dict[str, Schema] = {}


def parametrized(decorator):
    def wrapper(*args, **kwargs):
        def _decorator(func):
            return decorator(func, *args, **kwargs)

        return _decorator

    return wrapper


@parametrized
def inputs(schema, endpoint):
    inputs_schemas[endpoint] = schema()
    return schema


@parametrized
def output(schema, endpoint):
    output_schemas[endpoint] = schema()
    return schema


@parametrized
def tabular(func, endpoint):

    blueprint = Blueprint(endpoint, __name__)
    blueprints.append(blueprint)

    @blueprint.route(f"/{endpoint}", methods=["GET", "POST"])
    def _tabular():
        ischema = inputs_schemas.get(endpoint, None)
        oschema = output_schemas.get(endpoint, None)

        if request.method == "GET":
            return render_template(
                "base.html",
                inputs_template="tabular_inputs.html",
                output_template="tabular_output.html",
                inputs=[
                    {"name": name, "html": field_to_html(field, name)}
                    for name, field in ischema.fields.items()
                ],
            )

        inputs = request.get_json()
        json = True

        if not inputs:
            inputs = request.form
            json = False

        if ischema:
            inputs = ischema.load(inputs)

        output = func(**inputs)

        if oschema:
            output = oschema.dump(
                {
                    "result": output,
                    "version": "0.0.1",
                }
            )

        if not json:
            return render_template(
                "base.html",
                inputs_template="tabular_inputs.html",
                output_template="tabular_output.html",
                inputs=[
                    {
                        "name": name,
                        "html": field_to_html(
                            field=field, name=name, value=inputs[name]
                        ),
                    }
                    for name, field in ischema.fields.items()
                ],
                output=[
                    {"name": name, "value": value} for name, value in output.items()
                ],
            )

        return output

    return func


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )


blue = Blueprint("main", __name__)
blueprints.append(blue)


@blue.route("/image", methods=["GET", "POST"])
def upload_file():

    if request.method == "GET":
        return render_template(
            "base.html",
            inputs_template="image_inputs.html",
            output_template="image_output.html",
        )

    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files["file"]

    if file.filename == "":
        flash("No file selected")
        return redirect(request.url)

    if not allowed_file(file.filename):
        flash("File is not allowed")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    filepath = os.path.join(config.UPLOAD_FOLDER, filename)

    file.save(filepath)

    return render_template(
        "base.html",
        inputs_template="image_inputs.html",
        output_template="image_output.html",
        inputs=file,
        output=filepath,
    )


@blue.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(f"../../{config.UPLOAD_FOLDER}", filename)
