from flask import render_template, request

from .. import model  # noqa
from .config import app
from .endpoint import blueprints, sitemap


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        config=app.config,
        sitemap=sitemap(request),
        inputs=[],
        output=[],
        metadata={
            "name": "Home",
        },
    )


for blueprint in blueprints:
    app.register_blueprint(blueprint)
