from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from flasknet.database import get_db

authorization_views = Blueprint('auth', __name__)


@authorization_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        error = None
        username = request.form['username']
        if not username:
            error = 'Username is required.'
        if error is None:
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username, )
            ).fetchone()
            if user is None:
                error = "Username not found."
            else:
                session.clear()
                session['user'] = user['username']
                flash('Login successful.', 'success')
                return redirect(url_for('index'))

        flash('Login unsuccessful. ' + error, 'danger')

    return render_template('home.html', page='Home')


@authorization_views.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout successful.', 'success')
    return redirect(url_for('index'))
