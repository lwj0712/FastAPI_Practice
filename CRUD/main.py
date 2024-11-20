from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import itertools

app = FastAPI(
    title="CRUD API",
    description="API for CRUD",
    version="1.1.0",
)

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


@app.post("/items", response_model=Item, tags=["Item"])
async def create_item(item: Item):
    """
    item을 생성합니다.
    """
    item_id = next(id_counter)
    items[item_id] = item
    return item


@app.get("/items", response_model=List[Item], tags=["Item"])
async def read_items():
    """
    item 목록을 불러옵니다.
    """
    return list(items.values())


@app.get("/items/{item_id}", response_model=Item, tags=["Item"])
async def read_item(item_id: int):
    """
    item_id 값을 입력하여 특정 item 정보를 불러옵니다.
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.get("/items/search", response_model=List[Item], tags=["Item"])
async def search_items(name: str = Query(..., min_length=1)):
    """
    item 검색
    """
    results = [item for item in items.values() if item.name.lower() == name.lower()]
    if not results:
        raise HTTPException(
            status_code=404, detail="No items match the search criteria"
        )
    return results


@app.get("/items/filter", response_model=List[Item], tags=["Item"])
async def filter_items(category: str = Query(..., min_length=1)):
    """
    카테고리 필드에 대한 필터링
    """
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


@app.put("/items/{item_id}", response_model=Item, tags=["Item"])
async def update_item(item_id: int, item: ItemUpdate):
    """
    item 정보 업데이트
    기존에 있던 정보를 대체합니다.
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items[item_id]
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item.copy(update=update_data)
    items[item_id] = updated_item
    return updated_item


@app.delete("/items/{item_id}", response_model=Item, tags=["Item"])
async def delete_item(item_id: int):
    """
    item 삭제
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    item = items.pop(item_id)
    return item
