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
    return render_template('message.html', page='Message', received=received, sent=sent, action='message_user',
                           fields=[['receiver', 'max.mustermann'],
                                   ['message', 'Hello!']], submit='Send')


@message_views.route('/message_user', methods=['POST'])
def send():
    db = get_db()
    error = None
    sender = session.get('user')
    receiver = request.form['receiver']
    content = request.form['message']
    if not receiver:
        error = 'Receiver is required.'
    if not content:
        error = 'Message is required.'
    if error is None:
        try:
            db.execute(
                "INSERT INTO messages (sender, receiver, content) VALUES (?, ?, ?)",
                (sender, receiver, content))
            db.commit()
        except db.IntegrityError:
            error = "Not null error"
        else:
            flash('Message sent.', 'success')
            return redirect(url_for('message.message'))

    flash('Message unsent.', 'danger')
    return redirect(url_for('message.message'))
