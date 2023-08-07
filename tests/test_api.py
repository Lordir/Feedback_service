def test_register(client, app):
    assert client.get('/').status_code == 200
