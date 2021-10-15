import pytest
from flasknet.database import get_db


def test_register_success(app, client, action):
    assert client.get('/register').status_code == 200
    response = action.register()
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', ('mara.musterfrau', )
        ).fetchone()
        assert user is not None
        assert user['prename'] == 'Mara'
        assert user['surname'] == 'Musterfrau'


@pytest.mark.parametrize(('prename', 'surname', 'message'), (
    ('', 'Mustermann', b'Prename is required.'),
    ('Max', '', b'Surname is required.'),
    ('Max', 'Mustermann', b'Username is already registered.'),
))
def test_register_unsuccess(action, prename, surname, message):
    response = action.register(prename=prename, surname=surname)
    assert message in response.data
