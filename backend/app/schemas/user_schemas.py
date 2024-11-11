from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str


class UserLoginSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
