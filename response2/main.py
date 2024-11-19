from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Union

app = FastAPI()


class Item(BaseModel):
    id: str
    name: str
    price: float
    stock: str


items = []


@app.post(
    "/item/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    response_model_include={"id", "name", "price"},
)
async def create_item(item: Item):
    items.append(item)
    return item


@app.get("/item/")
async def item_list():
    return items
