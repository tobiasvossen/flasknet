from flask import g, session
from app.database import get_db


def test_register(app, client, registration):
    assert client.get('/register').status_code == 302
    response = registration.register()
    assert response.headers['Location'] == 'http://localhost/login'

    with app.app_context():
        user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', ('michael.jackson', )
        ).fetchone()
        assert user is not None
        assert user['prename'] == 'Michael'
        assert user['surname'] == 'Jackson'
