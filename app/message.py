from flask import (Blueprint, flash, g, redirect, render_template, request, session,
                   url_for)

from app.database import get_db

message_views = Blueprint('message', __name__)


@message_views.route('/message')
def message():
    username = session.get('user')
    received = get_db().execute(
        'SELECT * FROM messages WHERE receiver = ?', (username, )
    ).fetchall()
    sent = get_db().execute(
        'SELECT * FROM messages WHERE sender = ?', (username, )
    ).fetchall()
    return render_template('message.html', page='Message', received=received, sent=sent)
