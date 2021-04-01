from flask import Blueprint, request
from marshmallow import Schema

blueprints: list[Blueprint] = []
input_schemas: dict[str, Schema] = {}
output_schemas: dict[str, Schema] = {}


def parametrized(decorator):
    def wrapper(*args, **kwargs):
        def _decorator(func):
            return decorator(func, *args, **kwargs)

        return _decorator

    return wrapper


@parametrized
def input(schema, endpoint):
    input_schemas[endpoint] = schema()
    return schema


@parametrized
def output(schema, endpoint):
    output_schemas[endpoint] = schema()
    return schema


@parametrized
def tabular(func, endpoint):

    blueprint = Blueprint(endpoint, __name__)
    blueprints.append(blueprint)

    @blueprint.route(f"/{endpoint}", methods=["POST"])
    def tabular_endpoint():
        inputs = request.get_json()

        schema = input_schemas.get(endpoint, None)
        if schema is not None:
            inputs = schema.load(inputs)

        output = func(**inputs)

        schema = output_schemas.get(endpoint, None)
        if schema is not None:
            return schema.dump(
                {
                    "result": output,
                    "version": "0.0.1",
                }
            )
        else:
            return output

    return func
