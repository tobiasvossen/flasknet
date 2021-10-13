from flask import g, session
import pytest


def test_login_success(client, action):
    assert client.get('/login').status_code == 200
    response = action.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user'] == 'max.mustermann'
        assert g.user['username'] == 'max.mustermann'


@pytest.mark.parametrize(('username', 'message'), (
    ('', b'Username is required.'),
    ('max', b'Username not found.'),
))
def test_login_unsuccess(client, action, username, message):
    response = action.login(username=username)
    assert message in response.data


def test_logout(client, action):
    action.login()

    with client:
        action.logout()
        assert 'user' not in session


def test_index(client, action):
    response = client.get('/')
    assert b"Register" in response.data
    assert b"Login" in response.data

    action.login()
    response = client.get('/')
    assert b'Communications' in response.data
    assert b'Logout' in response.data
