def test_user_overview(client, action):
    action.login()
    response = client.get('/users')
    assert response.status_code == 200
    assert b'max.mustermann' in response.data


def test_new_user(client, action):
    response = client.get('/users/new')
    assert response.status_code == 200
