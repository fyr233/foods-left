import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from food.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/store', methods=('GET', 'POST'))
def store():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/store.html')




@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        phonenumber = request.form['phonenumber']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE user_phone = ?', (phonenumber,)
        ).fetchone()

        if user is None:
            error = 'Incorrect phone number.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_phone'] = user['user_phone']
            return redirect(url_for('index'))


    return render_template('auth/login.html',  error=error)


@bp.before_app_request
def load_logged_in_user():
    user_phone = session.get('user_phone')

    if user_phone is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE user_phone = ?', (user_phone,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


'''
装饰器(拦截器)
'''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view