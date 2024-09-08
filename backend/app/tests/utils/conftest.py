from typing import Generator

import pytest
from app.database import Base, get_db
from app.main import app
from app.tests.utils.overrides import override_get_db
from app.tests.utils.test_db import TestingSessionLocal, engine
from fastapi.testclient import TestClient

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db() -> Generator:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
