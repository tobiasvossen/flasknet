from app.authorization import authorization_views
from app.database import get_db
from app.message import message_views
from app.registration import registration_views
from flask import Flask
from flask import g, render_template, session
import os
import secrets


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasknet.sqlite'),
    )
    app.secret_key = secrets.token_urlsafe(16)
    app.register_blueprint(authorization_views, url_prefix='/')
    app.register_blueprint(message_views, url_prefix='/')
    app.register_blueprint(registration_views, url_prefix='/')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('home.html', page='Home')

    @app.route('/users')
    def users():
        users = get_db().execute(
            'SELECT username FROM user').fetchall()
        return render_template('users.html', page='Users', list=users, key='username')

    @ app.before_request
    def load_logged_in_user():
        username = session.get('user')

        if username is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECT * FROM user WHERE username = ?', (username, )
            ).fetchone()

    return app
