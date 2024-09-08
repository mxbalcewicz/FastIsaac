import pytest
from app.models.item_models import Item, ItemPool, Trinket
from sqlalchemy.orm import Session


@pytest.fixture
def itempool_fixture(db_session: Session):
    itempool = ItemPool(name="Test Pool")
    db_session.add(itempool)
    db_session.commit()
    db_session.refresh(itempool)
    return itempool


@pytest.fixture
def item_fixture(db_session: Session, itempool_fixture: ItemPool):
    item = Item(
        name="Test Item",
        description="A test item description",
        quote="This is a test quote",
        quality=1,
        item_pools=[itempool_fixture],  # Associate the item with an item pool
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item


@pytest.fixture
def trinket_fixture(db_session: Session):
    trinket = Trinket(
        name="Test Trinket",
        description="A test trinket description",
        quote="This is a trinket quote",
    )
    db_session.add(trinket)
    db_session.commit()
    db_session.refresh(trinket)
    return trinket
