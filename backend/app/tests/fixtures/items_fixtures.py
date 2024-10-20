import pytest
from app.tests.factories.item_factories import (
    ItemFactory,
    ItemPoolFactory,
    TrinketFactory,
)
from sqlalchemy.orm import Session


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
