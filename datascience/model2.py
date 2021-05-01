import functools
import inspect
from enum import Enum
from typing import Any, Callable, Literal, Optional, TypedDict, Union

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, create_model

app = FastAPI(
    title="My Datascience Project",
    description="Short description",
    version="2.5.0",
)


def std_default(default):
    return ... if default == inspect._empty else default


def default_to_form(default):
    return Form(std_default(default))


def is_model(cls):
    return issubclass(cls, BaseModel)


def model_to_form(model):
    model.__signature__ = model.__signature__.replace(
        parameters=[
            arg.replace(default=default_to_form(arg.default))
            for arg in model.__signature__.parameters.values()
        ]
    )
    return model


def extract_request_body(func: Callable[[...], Any]) -> dict[str, tuple[type, Any]]:
    params = inspect.signature(func).parameters
    return {
        k: (p.annotation, std_default(p.default))
        for k, p in params.items()
        if is_model(p.annotation)
    }


def body_to_form(body):
    return {k: (model_to_form(m), d) for k, (m, d) in body.items()}


def wraps(wrapped, postfix=None):
    def decorator(wrapper):

        print(inspect.signature(wrapper))
        print(wrapper.__qualname__)

        wrapper = functools.update_wrapper(
            wrapper,
            wrapped,
            assigned=("__module__", "__name__", "__qualname__", "__doc__"),
            updated=(),
        )
        wrapper.__name__ += f"_{postfix}" if postfix is not None else ""

        print(inspect.signature(wrapper))
        print(wrapper.__qualname__)

        return wrapper

    return decorator


def frontend(app, endpoint, response_model=None):
    app.mount("/static", StaticFiles(directory="datascience/api/static"), name="static")
    templates = Jinja2Templates(directory="templates")

    def decorator(func):
        body = extract_request_body(func)
        request_body = create_model("RequestBody", **body)
        request_form = create_model("RequestForm", **body_to_form(body))

        @app.get(endpoint, response_class=HTMLResponse)
        @wraps(func, postfix="form")
        def render(
            request: Request,
            inputs: Optional[request_body] = None,
            output: Optional[response_model] = None,
        ):
            return templates.TemplateResponse(
                "item.html",
                {
                    "request": request,
                    "inputs": inputs,
                    "output": output,
                },
            )

        @app.post(endpoint, response_model=response_model)
        @wraps(func, postfix="form")
        def form(form: request_form):
            return func(**form.dict())

        return func

    return decorator


class Formula(Enum):
    ADDITION = "addition"
    MULTIPLICATION = "multiplication"


class PredictIn(BaseModel):
    foo: bool
    bar: int
    x: float
    y: int
    formula: Formula
    image: str = ""


class PredictOut(BaseModel):
    result: float
    version: Optional[str] = app.version


@app.post("/predict", response_model=PredictOut)
@frontend(app, "/predict_f", response_model=PredictOut)
def predict(input: PredictIn):
    """
    Frickin' [sic]
    """
    if input.foo:
        return {"result": [9000]}

    res: list[float] = []

    if "addition" == input.formula:
        res.append(input.x + input.y)

    if "multiplication" == input.formula:
        res.append(input.x * input.y)

    return {"result": res}


if __name__ == "__main__":

    def f(input: PredictIn):
        pass

    for v in inspect.signature(f).parameters.values():
        print(type(v.annotation))

    print(
        {
            k: v.annotation
            for k, v in inspect.signature(f).parameters.items()
            if issubclass(v.annotation, BaseModel)
        }
    )

    print()

    for arg in inspect.signature(PredictIn).parameters.values():
        print(arg, arg.default == inspect._empty, "\n")

    Result = model_to_form(PredictIn)

    print(Result.__signature__.parameters, "\n")
