from flask import Flask

from .. import model  # noqa
from . import endpoint

app = Flask(__name__)

for blueprint in endpoint.blueprints:
    app.register_blueprint(blueprint)
