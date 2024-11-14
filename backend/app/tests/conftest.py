import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app
from app.settings import settings
from app.tests.factories.item_factories import (
    ItemFactory,
    ItemPoolFactory,
    TrinketFactory,
)
from app.tests.factories.user_factories import UserFactory

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
    for factory_class in (ItemPoolFactory, ItemFactory, TrinketFactory, UserFactory):
        factory_class._meta.sqlalchemy_session = db_session


@pytest.fixture
def user_fixtures(db_session):
    users = [UserFactory() for _ in range(5)]
    db_session.commit()
    return users


@pytest.fixture
def item_pool_fixtures(db_session: Session):
    item_pools = [ItemPoolFactory() for _ in range(5)]
    db_session.commit()
    return item_pools


@pytest.fixture
def item_fixtures(db_session: Session, item_pool_fixtures):
    items = []
    for _ in range(20):
        item_pool = item_pool_fixtures[_ % len(item_pool_fixtures)]
        item = ItemFactory(item_pools=[item_pool])
        items.append(item)
    db_session.commit()
    return items


@pytest.fixture
def trinket_fixtures(db_session: Session):
    trinkets = [TrinketFactory() for _ in range(20)]
    db_session.commit()
    return trinkets
