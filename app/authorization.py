from flask import (Blueprint, flash, g, redirect, render_template, request, session,
                   url_for)

from app.database import get_db

authorization_views = Blueprint('auth', __name__)


@authorization_views.route('/login')
def login():
    return render_template('login.html', page='Login')


@authorization_views.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout successful.', 'success')
    return redirect(url_for('index'))


@authorization_views.route('/auth_user', methods=['POST'])
def auth():
    username = request.form['username']
    user = get_db().execute(
        'SELECT * FROM user WHERE username = ?', (username, )
    ).fetchone()
    if user is not None:
        session['user'] = user['username']
        flash('Login successful.', 'success')
        return redirect(url_for('index'))
    else:
        flash('Login unsuccessful. Username not found.', 'danger')
        return redirect(url_for('auth.login'))
