from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import itertools

app = FastAPI()

id_counter = itertools.count(1)

items = {}


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str | None = None


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None


@app.post("/items", response_model=Item)
async def create_item(item: Item):
    item_id = next(id_counter)
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


@app.get("/items/search", response_model=List[Item])
async def search_items(name: str = Query(..., min_length=1)):
    results = [item for item in items.values() if item.name.lower() == name.lower()]
    if not results:
        raise HTTPException(
            status_code=404, detail="No items match the search criteria"
        )
    return results


@app.get("/items/filter", response_model=List[Item])
async def filter_items(category: str = Query(..., min_length=1)):
    results = [
        item
        for item in items.values()
        if item.category and item.category.lower() == category.lower()
    ]
    if not results:
        raise HTTPException(
            status_code=404, detail="No items found in the specified category"
        )
    return results


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
