def test_read_item(client):
    response = client.get("/item/")
    assert response.status_code == 201
