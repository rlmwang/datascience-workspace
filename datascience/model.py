from marshmallow import Schema, fields

from .api.endpoint import endpoint, inputs, output

model = [1, 2]


@endpoint("/predict", "tabular", "tabular")
def predict(x: float, y: int, b: bool):
    return x + b * y


@inputs("/predict")
class Inputs(Schema):
    x = fields.Float(required=True)
    y = fields.Float(missing=0)
    b = fields.Bool()

    class Meta:
        ordered = True


@output("/predict")
class Output(Schema):
    result = fields.Float(default=0)
    version = fields.String(default="latest")

    class Meta:
        ordered = True
