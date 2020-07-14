from fastapi import APIRouter, HTTPException, Path, BackgroundTasks
from services.schemas.users.UserSchema import UserCreate, UserModel
from services.schemas.items.ItemSchema import ItemModel
from services.models.UserModel import User
from services.libs.MailSmtp import MailSmtp
from typing import List

router = APIRouter()

class UserItems(UserModel):
    items: List[ItemModel] = []

@router.post('/user/create', status_code=201)
async def create_user(user: UserCreate):
    if User.query.filter_by(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user_model = User(**user.dict())
    user_model.save_to_db()
    return {"message": "Success create user"}

@router.get('/users', status_code=200, response_model=List[UserItems])
async def get_user():
    return User.query.all()

@router.get('/user/{user_id}', status_code=200, response_model=UserItems)
async def get_specific_user(user_id: int = Path(..., gt=0)):
    if (user := User.query.get(user_id)):
        return user

    raise HTTPException(status_code=404, detail="User not found")

@router.post('/user/send-email', status_code=202)
async def send_email(user: UserCreate, background_tasks: BackgroundTasks):
    background_tasks.add_task(MailSmtp.send_email,[user.email],'Test Email','email.html',name="test")

    return {"message": "Notification sent in the background"}
