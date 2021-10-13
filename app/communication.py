from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from app.database import get_db

communication_views = Blueprint('communication', __name__)


@communication_views.route('/communications')
def communications():
    username = session.get('user')
    received = get_db().execute(
        'SELECT * FROM messages WHERE receiver = ?', (username, )
    ).fetchall()
    sent = get_db().execute(
        'SELECT * FROM messages WHERE sender = ?', (username, )
    ).fetchall()
    return render_template('communication.html', page='Communication', received=received, sent=sent, action='message',
                           fields=[
                               ['receiver', 'mara.musterfrau'],
                               ['content', 'Hello!']],
                           static_fields=[['sender', username]],
                           submit='Send')


@communication_views.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        db = get_db()
        error = None
        sender = request.form['sender']
        receiver = request.form['receiver']
        content = request.form['content']
        if sender != session.get('user'):
            error = 'Sender not found.'
        if not receiver:
            error = 'Receiver is required.'
        if not content:
            error = 'Message is required.'
        if error is None:
            db.execute(
                "INSERT INTO messages (sender, receiver, content) VALUES (?, ?, ?)",
                (sender, receiver, content))
            db.commit()
            flash('Message sent.', 'success')
            return redirect(url_for('communication.message'))

        flash('Message unsent. ' + error, 'danger')

    return render_template('home.html', page='Home')
