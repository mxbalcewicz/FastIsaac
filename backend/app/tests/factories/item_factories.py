import factory
from app.models.item_models import Item, ItemPool, Trinket


class ItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Item
        sqlalchemy_session_persistence = "commit"

    wiki_id = factory.Faker("word")
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    quote = factory.Faker("sentence")
    quality = factory.Faker("random_int", min=0, max=3)


class ItemPoolFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ItemPool
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("word")


class TrinketFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Trinket
        sqlalchemy_session_persistence = "commit"

    wiki_id = factory.Faker("word")
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    quote = factory.Faker("sentence")
