from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import AuthHandler
from app.database import get_db
from app.models.user_models import User
from app.operations.user_operations import create_user, get_user_by_email
from app.schemas.user_schemas import UserLoginSchema, UserRegisterSchema

router = APIRouter()


@router.post("/register")
async def register(user: UserRegisterSchema, db: AsyncSession = Depends(get_db)):
    await user.validate_passwords_match(password=user.password, password_confirm=user.password_confirm)
    await user.validate_unique_email(db_session=db, email=user.email)
    await user.validate_unique_username(db_session=db, username=user.username)

    new_user: User = await create_user(db, user)
    return AuthHandler.sign_token(new_user.email)


@router.post("/login")
async def login(user: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    async def check_user(data: UserLoginSchema):
        user = await get_user_by_email(db, email=data.email)
        if user and user.email == data.email and user.password == data.password:
            return True
        return False

    if await check_user(user):
        return AuthHandler.sign_token(user.email)

    raise HTTPException(status_code=400, detail="Wrong credentials.")


@router.post("/refresh-token")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    refresh_token = credentials.credentials
    return AuthHandler.refresh_token(refresh_token)
