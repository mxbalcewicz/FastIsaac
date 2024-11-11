from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import AuthHandler
from app.database import get_db
from app.models.user_models import User
from app.operations.user_operations import create_user, get_user_by_email
from app.schemas.user_schemas import UserLoginSchema, UserRegisterSchema
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register")
def register(user: UserRegisterSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    user = create_user(db, user)
    return AuthHandler.sign_token(user.email)


@router.post("/login")
def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    def check_user(data: UserLoginSchema):
        user = get_user_by_email(db, email=data.email)
        if user:
            if user.email == data.email and user.password == data.password:
                return True
        return False

    if check_user(user):
        return AuthHandler.sign_token(user.email)
    raise HTTPException(status_code=400, detail="Wrong credentials.")


@router.post("/refresh-token")
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    refresh_token = credentials.credentials
    return AuthHandler.refresh_token(refresh_token)
