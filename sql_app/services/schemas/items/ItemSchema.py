from pydantic import BaseModel, Field
from typing import Optional

############################################
# ============== ITEM SCHEMAS ==============
############################################
class ItemBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, min_length=1)

class ItemCreate(ItemBase):
    pass

class ItemModel(ItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
