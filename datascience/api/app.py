from flask import Flask

from .. import model  # noqa
from . import config, endpoint

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER

for blueprint in endpoint.blueprints:
    app.register_blueprint(blueprint)
