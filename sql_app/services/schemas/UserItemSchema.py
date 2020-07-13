from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List

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

class ItemUser(ItemModel):
    user: UserModel

############################################
# ============== USER SCHEMAS ==============
############################################
class UserBase(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=3)

class UserCreate(UserBase):
    pass

class UserModel(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserItems(UserModel):
    items: List[ItemModel] = []


ItemUser.update_forward_refs()
