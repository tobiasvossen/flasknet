import os
import secrets

from flask import Flask, g, render_template, session

from flasknet.authorization import authorization_views
from flasknet.communication import communication_views
from flasknet.database import get_db, init_db, close_db
from flasknet.registration import registration_views
from flasknet.user import user_views


__version__ = '0.1.0'
__author__ = 'Tobias Vossen'


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasknet.sqlite'),
    )
    app.secret_key = secrets.token_urlsafe(16)

    app.register_blueprint(authorization_views, url_prefix='/')
    app.register_blueprint(communication_views, url_prefix='/')
    app.register_blueprint(registration_views, url_prefix='/')
    app.register_blueprint(user_views, url_prefix='/')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

    @app.route('/')
    def index():
        return render_template('home.html', page='Home')

    @app.before_request
    def set_user_from_session():
        """Checks wether our session has an active and therefore logged in user."""
        username = session.get('user')

        if username is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECT * FROM user WHERE username = ?', (username, )
            ).fetchone()

    return app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
