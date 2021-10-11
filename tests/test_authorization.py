from flask import g, session


def test_login(client, auth):
    assert client.get('/login').status_code == 302
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user'] == 'max.mustermann'
        assert g.user['username'] == 'max.mustermann'


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user' not in session


def test_index(client, auth):
    response = client.get('/')
    assert b"Register" in response.data
    assert b"Login" in response.data

    auth.login()
    response = client.get('/')
    assert b'Message' in response.data
    assert b'Logout' in response.data
