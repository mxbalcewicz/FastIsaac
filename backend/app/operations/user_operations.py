from app.auth.auth_bearer import AuthHandler, JWTBearer
from app.database import get_db
from app.models.user_models import User
from app.schemas.user_schemas import UserRegisterSchema
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user: UserRegisterSchema):
    hashed_password = get_password_hash(user.password)

    new_user = User(username=user.username, email=user.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_current_user(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    payload = AuthHandler.decode_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid or expired token.")
    user = db.query(User).filter(User.email == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user
