from flask import Flask
from flask import render_template
import secrets


def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_urlsafe(16)

    @app.route('/')
    def index():
        return render_template('landing.html', page='Landing')

    return app
