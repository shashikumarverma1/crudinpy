from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class UpdateItem(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
