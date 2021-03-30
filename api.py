from inspect import signature

from flask import Flask
from flask_restful import Api, Resource, reqparse

model = [1, 2]


def predict(model, x: float, y):
    return model[0] * x + model[1] * y


parameters = signature(predict).parameters
features = {k: v.annotation for k, v in parameters.items()}
del features["model"]


class Prediction(Resource):
    def __init__(self, features):
        self.reqparser = reqparse.RequestParser()
        for feature, dtype in features.items():
            self.reqparser.add_argument(
                feature,
                type=dtype,
                required=True,
                location="json",
                help=f"Feature '{feature}' of type '{dtype.__name__}' is missing",
            )
        super().__init__()

    def post(self):
        return predict(model, **self.reqparser.parse_args())


app = Flask(__name__)
api = Api(app)
api.add_resource(Prediction, "/predict", resource_class_args=(features,))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
