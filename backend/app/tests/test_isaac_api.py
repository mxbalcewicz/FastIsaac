from app.tests.utils.conftest import client


def test_read_item(client):
    response = client.get("/item/")
    print("Response Status Code:", response.status_code)
    print("Response JSON Body:", response.json())
    assert response.status_code == 200
