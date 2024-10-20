import factory
from app.models.item_models import Item, ItemPool, Trinket
from app.tests.factories.item_factories import (
    ItemFactory,
    ItemPoolFactory,
    TrinketFactory,
)
from app.tests.fixtures.items_fixtures import (
    item_fixtures,
    item_pool_fixtures,
    trinket_fixtures,
)
from httpx import Response


class TestIsaacAPI:

    class Endpoints:
        item = "item"
        item_pool = "item_pool"
        trinket = "trinket"

    def _assert_item_response(self, db_object, response_object):
        assert db_object.id == response_object["id"]
        assert db_object.name == response_object["name"]
        assert db_object.description == response_object["description"]
        assert db_object.quote == response_object["quote"]
        assert db_object.quality == response_object["quality"]

    def _assert_item_pool_response(self, db_object, response_object):
        assert db_object.id == response_object["id"]
        assert db_object.name == response_object["name"]

    def _assert_trinket_response(self, db_object, response_object):
        assert db_object.id == response_object["id"]
        assert db_object.name == response_object["name"]
        assert db_object.description == response_object["description"]
        assert db_object.quote == response_object["quote"]

    def _assert_object_response(self, query: list, response: Response, assert_function):
        response_data = response.json()
        if isinstance(response_data, list):
            for db_item, data in zip(query, response_data):
                assert_function(db_item, data)
        else:
            assert_function(query, response_data)

    def _get_all_model_instances(self, db_session, model_class):
        return db_session.query(model_class).all()

    def _get_non_existing_id(self, db_session, model_class):
        max_id = (
            db_session.query(model_class.id).order_by(model_class.id.desc()).first()
        )
        if max_id:
            return max_id[0] + 1
        else:
            return 1

    def test_item__get__list(self, client, db_session, item_fixtures):
        response = client.get(url=self.Endpoints.item)
        query = self._get_all_model_instances(db_session, Item)

        assert len(query) == len(response.json())
        print(response.json())
        assert response.status_code == 200
        self._assert_object_response(query, response, self._assert_item_response)

    def test_item__get__detail(self, client, db_session, item_fixtures):
        item = db_session.query(Item).first()
        response = client.get(url=f"{self.Endpoints.item}/{item.id}")

        assert response.status_code == 200
        self._assert_item_response(item, response.json())

    def test_item__delete(self, client, db_session, item_fixtures):
        item = db_session.query(Item).first()
        response = client.delete(url=f"{self.Endpoints.item}/{item.id}")
        item_in_db = db_session.get(Item, item.id)

        assert response.status_code == 200
        assert item_in_db is None

    def test_item__get__detail__non_existing(self, client, db_session):
        non_existing_id = self._get_non_existing_id(db_session, Item)
        response = client.get(url=f"{self.Endpoints.item}/{non_existing_id}")

        assert response.status_code == 404

    def test_item__delete__non_existing(self, client, db_session):
        non_existing_id = self._get_non_existing_id(db_session, Item)
        response = client.delete(url=f"{self.Endpoints.item}/{non_existing_id}")

        assert response.status_code == 404

    def test_trinket__get__list(self, client, db_session, trinket_fixtures):
        response: Response = client.get(url=self.Endpoints.trinket)
        query = self._get_all_model_instances(db_session, Trinket)

        assert len(query) == len(response.json())
        assert response.status_code == 200
        self._assert_object_response(query, response, self._assert_trinket_response)

    def test_trinket__get__detail(self, client, db_session, trinket_fixtures):
        trinket = db_session.query(Trinket).first()
        response = client.get(url=f"{self.Endpoints.trinket}/{trinket.id}")

        assert response.status_code == 200
        self._assert_trinket_response(trinket, response.json())

    def test_trinket__delete(self, client, db_session, trinket_fixtures):
        trinket = db_session.query(Trinket).first()
        response = client.delete(url=f"{self.Endpoints.trinket}/{trinket.id}")
        trinket_in_db = db_session.get(Trinket, trinket.id)

        assert response.status_code == 200
        assert trinket_in_db is None

    def test_trinket__get__detail__non_existing(self, client, db_session):
        non_existing_id = self._get_non_existing_id(db_session, Trinket)
        response = client.get(url=f"{self.Endpoints.trinket}/{non_existing_id}")
        assert response.status_code == 404

    def test_trinket__delete__non_existing(self, client, db_session):
        non_existing_id = self._get_non_existing_id(db_session, Trinket)
        response = client.delete(url=f"{self.Endpoints.trinket}/{non_existing_id}")
        assert response.status_code == 404

    def test_item_pool__get__list(self, client, db_session, item_pool_fixtures):
        response = client.get(url=self.Endpoints.item_pool)
        query = self._get_all_model_instances(db_session, ItemPool)

        assert len(query) == len(response.json())
        assert response.status_code == 200
        self._assert_object_response(query, response, self._assert_item_pool_response)

    def test_item_pool__get__detail(self, client, db_session, item_pool_fixtures):
        item_pool = db_session.query(ItemPool).first()
        response = client.get(url=f"{self.Endpoints.item_pool}/{item_pool.id}")

        assert response.status_code == 200
        self._assert_item_pool_response(item_pool, response.json())

    def test_item_pool__delete(self, client, db_session, item_pool_fixtures):
        item_pool = db_session.query(ItemPool).first()
        response = client.delete(url=f"{self.Endpoints.item_pool}/{item_pool.id}")
        item_pool_in_db = db_session.get(ItemPool, item_pool.id)

        assert response.status_code == 200
        assert item_pool_in_db is None

    def test_item_pool__get__detail__non_existing(self, client, db_session):
        non_existing_id = self._get_non_existing_id(db_session, ItemPool)
        response = client.get(url=f"{self.Endpoints.item_pool}/{non_existing_id}")

        assert response.status_code == 404

    def test_item_pool__delete__non_existing(self, client, db_session):
        non_existing_id = self._get_non_existing_id(db_session, ItemPool)
        response = client.delete(url=f"{self.Endpoints.item_pool}/{non_existing_id}")

        assert response.status_code == 404
