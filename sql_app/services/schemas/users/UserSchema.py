from pydantic import BaseModel, Field

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
