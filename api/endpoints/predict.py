from flask import Blueprint, request
from marshmallow import Schema, ValidationError, fields

predict_api = Blueprint("predict_api", __name__)


model = [1, 2]


def predict(model, x: float, y):
    return model[0] * x + model[1] * y


class InputSchema(Schema):
    x = fields.Float(required=True)
    y = fields.Int(required=True)


class OutputSchema(Schema):
    result = fields.Float()
    version = fields.String()


in_schema = InputSchema()
out_schema = OutputSchema()


@predict_api.route("/predict", methods=["POST"])
def _predict():
    json_data = request.get_json()
    try:
        data = in_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    result = predict(model, **data)
    return out_schema.dump(
        {
            "result": result,
            "version": "0.0.1",
        }
    )
