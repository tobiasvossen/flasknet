from flask import g, session
from app.database import get_db
import pytest


def test_message_success(app, client, action):
    action.login()
    assert client.get('/message').status_code == 200
    response = action.message()
    assert response.headers['Location'] == 'http://localhost/message'

    with app.app_context():
        message = get_db().execute(
            'SELECT * FROM messages WHERE sender = ? AND receiver = ?', ('max.mustermann', 'mara.musterfrau')
        ).fetchone()
        assert message is not None
        assert message['sender'] == 'max.mustermann'
        assert message['receiver'] == 'mara.musterfrau'


@pytest.mark.parametrize(('sender', 'receiver', 'content', 'message'), (
    ('max.mustermann', '', 'Hello, Mara!', b'Receiver is required.'),
    ('', 'mara.musterfrau', 'Hello, Mara!', b'Sender not found.'),
    ('max.mustermann', 'mara.musterfrau', '', b'Message is required.')
))
def test_message_unsuccess(action, sender, receiver, content, message):
    response = action.message(sender=sender, receiver=receiver, content=content)
    assert message in response.data


def test_message_overview(client, action):
    action.login()
    response = client.get('/communications')
    assert response.status_code == 200
    assert b'Hello Mara.' in response.data
