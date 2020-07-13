from fastapi import APIRouter, Path, HTTPException
from services.schemas.items.ItemSchema import ItemCreate, ItemModel
from services.schemas.users.UserSchema import UserModel
from services.models.UserModel import User
from services.models.ItemModel import Item
from typing import List

router = APIRouter()

class ItemUser(ItemModel):
    user: UserModel

@router.post('/item/create/{user_id}', status_code=201)
async def create_item(items: ItemCreate,user_id: int = Path(..., gt=0)):
    if (user := User.query.get(user_id)):
        item_model = Item(user_id=user.id, **items.dict())
        item_model.save_to_db()

        return {"message": "Success create item"}

    raise HTTPException(status_code=404, detail="User not found")

@router.get('/item/{item_id}', status_code=200, response_model=ItemUser)
async def get_specific_item(item_id: int = Path(..., gt=0)):
    if (item := Item.query.get(item_id)):
        return item

    raise HTTPException(status_code=404, detail="Item not found")

@router.get('/items', status_code=200, response_model=List[ItemUser])
async def get_items():
    items = Item.query.all()
    return items
