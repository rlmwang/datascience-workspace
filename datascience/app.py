from flask import Flask

from . import model  # noqa
from .api import endpoint

app = Flask(__name__)

for blueprint in endpoint.blueprints:
    app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(host="127.0.0.1", use_reloader=True, debug=True)
