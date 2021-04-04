from .. import model  # noqa
from .config import app
from .endpoint import blueprints

for blueprint in blueprints:
    app.register_blueprint(blueprint)
