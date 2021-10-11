import os
import tempfile

import pytest
from app import create_app
from app.database import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'tests/test_data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='max.mustermann'):
        return self._client.post('/login', data={'username': username})

    def logout(self):
        return self._client.get('/logout')

class RegistrationActions(object):
    def __init__(self, client):
        self._client = client

    def register(self, prename='Michael', surname='Jackson'):
        return self._client.post('/register_user', data={'prename': prename, 'surname': surname})
    

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def registration(client):
    return RegistrationActions(client)
