from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreateOut(BaseModel):
    id: int
    email: EmailStr
    admin: bool

    class Config:
        orm_mode = True
