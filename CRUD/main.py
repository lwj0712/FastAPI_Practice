from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

items = {}


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None


@app.post("/items/{item_id}", response_model=Item)
async def create_item(item_id: int, item: Item):
    if item_id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item_id] = item
    return item


@app.get("/items", response_model=List[Item])
async def read_items():
    return list(items.values())


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items[item_id]
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item.copy(update=update_data)
    items[item_id] = updated_item
    return updated_item


@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    item = items.pop(item_id)
    return item
