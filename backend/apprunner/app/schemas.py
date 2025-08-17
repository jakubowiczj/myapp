from pydantic import BaseModel, Field
from typing import Dict, Any

class ItemIn(BaseModel):
    body: Dict[str, Any] = Field(default_factory=dict)

class ItemOut(BaseModel):
    pk: str
    body: Dict[str, Any]
