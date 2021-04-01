from marshmallow import Schema, fields

from .api import endpoint

model = [1, 2]


@endpoint.tabular("predict")
def predict(x: float, y: int):
    return model[0] * x + model[1] * y


@endpoint.input("predict")
class Inputs(Schema):
    x = fields.Float(required=True)
    y = fields.Int(required=True)


@endpoint.output("predict")
class Output(Schema):
    result = fields.Float()
    version = fields.String()
