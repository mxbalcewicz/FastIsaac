import time
from typing import Dict

import jwt
from fastapi import HTTPException

from app.settings import settings


class AuthHandler:
    JWT_SECRET = settings.JWT_SECRET
    JWT_ALGORITHM = settings.JWT_ALGORITHM
    ACCESS_EXPIRE_TIME = 1200  # 20 mins
    REFRESH_EXPIRE_TIME = 86400  # 1 day

    @staticmethod
    def token_response(access_token: str, refresh_token: str = None):
        response = {"access_token": access_token}
        if refresh_token:
            response["refresh_token"] = refresh_token
        return response

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, AuthHandler.JWT_SECRET, algorithms=[AuthHandler.JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except jwt.DecodeError:
            return {}

    @staticmethod
    def sign_token(user_id: str) -> Dict[str, str]:
        access_payload = {
            "user_id": user_id,
            "expires": time.time() + AuthHandler.ACCESS_EXPIRE_TIME,
        }
        refresh_payload = {
            "user_id": user_id,
            "expires": time.time() + AuthHandler.REFRESH_EXPIRE_TIME,
        }
        access_token = jwt.encode(access_payload, AuthHandler.JWT_SECRET, algorithm=AuthHandler.JWT_ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, AuthHandler.JWT_SECRET, algorithm=AuthHandler.JWT_ALGORITHM)

        return AuthHandler.token_response(access_token, refresh_token)

    @staticmethod
    def refresh_token(refresh_token: str) -> Dict[str, str]:
        decoded_refresh = AuthHandler.decode_token(refresh_token)
        if not decoded_refresh:
            raise HTTPException(status_code=403, detail="Invalid or expired refresh token.")

        user_id = decoded_refresh["user_id"]
        return AuthHandler.sign_token(user_id)
