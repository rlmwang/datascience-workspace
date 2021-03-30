"""
curl -i -H "Content-Type: application/json" -X POST \
     -d '{"x": 3.14, "y": 2}' 127.0.0.1:5000/predict
"""
from flask import Flask, request
from marshmallow import Schema, ValidationError, fields

model = [1, 2]


def predict(model, x: float, y):
    return model[0] * x + model[1] * y


class InputSchema(Schema):
    x = fields.Float(required=True)
    y = fields.Int(required=True)


class OutputSchema(Schema):
    result = fields.Float()


in_schema = InputSchema()
out_schema = OutputSchema()

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def _predict():
    json_data = request.get_json()
    try:
        data = in_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    result = predict(model, **data)
    return out_schema.dump({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=True, debug=True)
