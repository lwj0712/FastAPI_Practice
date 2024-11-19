from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


items = []


@app.post("/item/")
async def create_item(item: Item):
    items.append(item)
    return {"message": "Item created successfully", "item": item}


@app.get("/item/")
async def read_items():
    return items


@app.get("/item/{item_id}")
async def read_item(item_id: int):
    if 0 <= item_id < len(items):
        return items[item_id]
    raise HTTPException(status_code=404, detail="Item not found")
