from app.auth import auth_views
from app.database import get_db
from flask import Flask
from flask import g, render_template, session
import os
import secrets


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasknet.sqlite'),
    )
    app.secret_key = secrets.token_urlsafe(16)
    app.register_blueprint(auth_views, url_prefix='/')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('landing.html', page='Landing')

    @app.route('/users')
    def users():
        users = get_db().execute(
            'SELECT * FROM user').fetchall()
        return render_template('list.html', list=users)

    @app.before_request
    def load_logged_in_user():
        username = session.get('user')

        if username is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECT * FROM user WHERE username = ?', (username, )
            ).fetchone()

    return app
