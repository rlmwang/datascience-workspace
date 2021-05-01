from enum import Enum
from typing import Optional, TypedDict

from fastapi import FastAPI
from pydantic import BaseModel, Field


class Switch(Enum):
    a = "a"
    b = "b"
    c = "c"


class Item(TypedDict):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: list[float]
    switch: Switch
    is_offer: Optional[bool] = None


class Output(TypedDict):
    item_name: str


app = FastAPI()


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/{item_id}", response_model=Output)
async def update_item(item_id: int, item: Item, item2: Item):
    return {
        "item_name": "foo",
    }
