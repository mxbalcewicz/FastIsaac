from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.orm import Session

from app.models.user_models import User


class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def validate_passwords_match(cls, password, password_confirm):
        if password != password_confirm:
            raise HTTPException(status_code=400, detail="Passwords do not match")

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
