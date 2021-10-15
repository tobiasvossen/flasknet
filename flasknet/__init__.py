import os
import argparse
from typing import ClassVar

from flask import Flask, g, render_template, session

from flasknet.authorization import authorization_views
from flasknet.communication import communication_views
from flasknet.config import DevelopmentConfig, ProductionConfig, TestingConfig
from flasknet.database import close_db, get_db, init_app, init_db
from flasknet.registration import registration_views
from flasknet.user import user_views


def create_app(config='testing', database=None):
    app = Flask(__name__)
    app.name = 'FlaskNet'
    app.register_blueprint(authorization_views, url_prefix='/')
    app.register_blueprint(communication_views, url_prefix='/')
    app.register_blueprint(registration_views, url_prefix='/')
    app.register_blueprint(user_views, url_prefix='/')

    if config == 'development':
        app.config.from_object(DevelopmentConfig())
    elif config == 'production':
        app.config.from_object(ProductionConfig())
    else:
        app.config.from_object(TestingConfig())

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if database is None:
        app.config.update(DATABASE=os.path.join(app.instance_path, 'flasknet.sqlite'))
    else:
        app.config.update(DATABASE=database)

    app.teardown_appcontext(close_db)
    with app.app_context():
        init_app(app)

    @ app.route('/')
    def index():
        return render_template('home.html', page='Home')

    @ app.before_request
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
    parser = argparse.ArgumentParser(prog='A simple social network made with Flask.')
    parser.add_argument('-config', choices=['development',
                        'production', 'testing'], default='production', help='Please choose a configuration.')
    args = parser.parse_args()
    app = create_app(config=args.config)
    app.run()


if __name__ == '__main__':
    main()
