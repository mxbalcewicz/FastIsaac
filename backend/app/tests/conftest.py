import pytest
from app.core.settings import settings
from app.database import Base, get_db
from app.main import app
from app.tests.factories.item_factories import (
    ItemFactory,
    ItemPoolFactory,
    TrinketFactory,
)
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine(settings.postgres_test_url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def set_session_for_factories(db_session):
    for factory_class in (ItemPoolFactory, ItemFactory, TrinketFactory):
        factory_class._meta.sqlalchemy_session = db_session
