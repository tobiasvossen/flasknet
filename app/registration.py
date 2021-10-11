from flask import (Blueprint, flash, g, redirect, render_template, request, session,
                   url_for)

from app.database import get_db

registration_views = Blueprint('register', __name__)


@registration_views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        error = None
        prename = request.form['prename']
        surname = request.form['surname']
        if not surname:
            error = 'Surname is required.'
        if not prename:
            error = 'Prename is required.'
        if error is None:
            username = prename.lower() + "." + surname.lower()
            try:
                db.execute(
                    "INSERT INTO user (username, prename, surname) VALUES (?, ?, ?)",
                    (username, prename, surname))
                db.commit()
            except db.IntegrityError:
                error = "Username is already registered."
            else:
                flash('Registration successful.', 'success')
                return redirect(url_for('auth.login'))

        flash('Registration unsuccessful. ' + error, 'danger')

    return redirect(url_for('index'))
