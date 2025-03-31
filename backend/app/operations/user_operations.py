from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.auth_bearer import AuthHandler, JWTBearer
from app.database import get_db
from app.models.user_models import User
from app.schemas.user_schemas import UserRegisterSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def create_user(db: AsyncSession, user: UserRegisterSchema):
    hashed_password = await get_password_hash(user.password)

    new_user = User(username=user.username, email=user.email, password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_current_user(token: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)):
    payload = AuthHandler.decode_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid or expired token.")

    result = await db.execute(select(User).filter(User.email == payload["user_id"]))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user
