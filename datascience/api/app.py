from flask import render_template, request
from markdown import markdown

from .. import model  # noqa
from .config import app
from .endpoint import blueprints, sitemap

with open("./README.md", "r", encoding="utf-8") as file:
    text = file.read()
readme = markdown(text, extensions=["fenced_code"])


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        config=app.config,
        sitemap=sitemap(request),
        inputs=[],
        output=[],
        metadata={"name": "Home"},
        readme=readme,
    )


for blueprint in blueprints:
    app.register_blueprint(blueprint)
