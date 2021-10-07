from flask import (Blueprint, g, redirect, render_template, request, session,
                   url_for)

from app.database import get_db

auth_views = Blueprint('auth', __name__)


@auth_views.route('/login')
def login():
    return render_template('login.html', page='Login')


@auth_views.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@auth_views.route('/auth_user', methods=['POST'])
def auth():
    username = request.form['username']
    user = get_db().execute(
        'SELECT * FROM user WHERE username = ?', (username, )
    ).fetchone()
    if user is not None:
        session['user'] = user['username']
        return redirect(url_for('index'))
    else:
        return redirect(url_for('auth.login'))
