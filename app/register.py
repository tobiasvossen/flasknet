from flask import (Blueprint, flash, g, redirect, render_template, request, session,
                   url_for)

from app.database import get_db

register_views = Blueprint('register', __name__)


@register_views.route('/register')
def register():
    return render_template('register.html', page='Registration')


@register_views.route('/register_user', methods=['POST'])
def register_user():
    db = get_db()
    error = None
    prename = request.form['prename']
    surname = request.form['surname']
    if not surname:
        error = 'Prename is required.'
    if not prename:
        error = 'Surname is required.'
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
            flash('Registration successful.')
            return redirect(url_for('auth.login'))

    flash(error)
    return redirect(url_for('register.register'))
