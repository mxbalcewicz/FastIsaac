class TestIsaacAPI:

    class Endpoints:
        item = "item"
        item_pool = "item_pool"
        trinket = "trinket"

    def test_item__get__list(self, client):
        response = client.get(url=self.Endpoints.item)
        assert response.status_code == 200

    def test_item_pool__get__list(self, client):
        response = client.get(url=self.Endpoints.item_pool)
        assert response.status_code == 200

    def test_trinket__get__list(self, client):
        response = client.get(url=self.Endpoints.trinket)
        assert response.status_code == 200
