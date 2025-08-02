from fastapi import APIRouter, HTTPException
from bson import ObjectId

from db.db import collection
from modals.itemModal import Item, UpdateItem

router = APIRouter()

# Helper to convert Mongo _id to string
def serialize_item(item):
    item["_id"] = str(item["_id"])
    return item

@router.post("/items")
async def create_item(item: Item):
    result = await collection.insert_one(item.dict())
    return {"id": str(result.inserted_id)}

@router.get("/items")
async def get_items():
    items = await collection.find().to_list(100)
    return [serialize_item(item) for item in items]

@router.get("/items/{item_id}")
async def get_item(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return serialize_item(item)
    raise HTTPException(status_code=404, detail="Item not found")

@router.put("/items/{item_id}")
async def update_item(item_id: str, updated_item: UpdateItem):
    update_data = {k: v for k, v in updated_item.dict().items() if v is not None}
    result = await collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})
    if result.modified_count:
        return {"msg": "Item updated"}
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return {"msg": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
