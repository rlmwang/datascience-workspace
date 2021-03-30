from flask import Flask

from .endpoints.predict import predict_api

app = Flask(__name__)
app.register_blueprint(predict_api)


if __name__ == "__main__":
    app.run(host="127.0.0.1", use_reloader=True, debug=True)
