from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, ValidationInfo, field_validator
from sqlalchemy.orm import Session

from app.models.user_models import User


class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str

    class Config:
        orm_mode = True

    @field_validator("password_confirm")
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("passwords do not match")
        return v

    @classmethod
    def validate_unique_email(cls, db_session: Session, email: str):
        user = db_session.query(User).filter(User.email == email).first()
        if user:
            raise HTTPException(status_code=400, detail="Email is already registered")

    @classmethod
    def validate_unique_username(cls, db_session: Session, username: str):
        user = db_session.query(User).filter(User.username == username).first()
        if user:
            raise HTTPException(status_code=400, detail="Username is already taken")


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
