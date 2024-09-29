# backend/tests/utils/overrides.py

from typing import Generator

from app.database import get_db
from sqlalchemy.orm import Session

# from backend.app.tests.conftest import TestingSessionLocal


# def override_get_db() -> Generator[Session, None, None]:
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()
