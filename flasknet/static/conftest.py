import os
import tempfile

import pytest
from flasknet import create_app
from flasknet.database import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'tests/test_data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


class Actions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='max.mustermann'):
        return self._client.post('/login', data={'username': username})

    def logout(self):
        return self._client.get('/logout')

    def register(self, prename='Mara', surname='Musterfrau'):
        return self._client.post('/register', data={'prename': prename, 'surname': surname})

    def message(self, sender='max.mustermann', receiver='mara.musterfrau', content='Hello, Mara!'):
        return self._client.post('/message', data={'sender': sender, 'receiver': receiver, 'content': content})


@ pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(config='testing', database=db_path)

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@ pytest.fixture
def client(app):
    return app.test_client()


@ pytest.fixture
def runner(app):
    return app.test_cli_runner()


@ pytest.fixture
def action(client):
    return Actions(client)


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
