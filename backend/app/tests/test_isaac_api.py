from app.models.item_models import Item, ItemPool, Trinket
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

    def _assert_item_response(self, item, response):
        pass

    def _assert_item_pool_response(self, item_pool, response):
        pass

    def _assert_trinket_response(self, query: list, response: Response):
        response_data = response.json()
        if isinstance(response_data, list):
            for data, db_item in zip(response_data, query):
                assert db_item.id == data["id"]
                assert db_item.name == data["name"]
                assert db_item.description == data["description"]
                assert db_item.quote == data["quote"]

    def _get_all_model_instances(self, db_session, model_class):
        return db_session.query(model_class).all()

    def test_item__get__list(self, client, item_fixtures):
        response = client.get(url=self.Endpoints.item)
        assert response.status_code == 200

    def test_item_pool__get__list(self, client, item_pool_fixtures):
        response = client.get(url=self.Endpoints.item_pool)
        assert response.status_code == 200

    def test_trinket__get__list(self, client, db_session, trinket_fixtures):
        response: Response = client.get(url=self.Endpoints.trinket)
        query = self._get_all_model_instances(db_session, Trinket)
        assert len(query) == len(response.json())
        assert response.status_code == 200
        self._assert_trinket_response(query, response)
