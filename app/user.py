from flask import (Blueprint, g, render_template, request, session)

from app.database import get_db

user_views = Blueprint('user', __name__)


@user_views.route('/users')
def users():
    users = get_db().execute(
        'SELECT username FROM user').fetchall()
    return render_template('users.html', page='Users', list=users, key='username')


@user_views.route('/users/new')
def new_user():
    return render_template('register.html', page='Registration', action='register',
                           fields=[['prename', 'Max'],
                                   ['surname', 'Mustermann']], submit='Register')
