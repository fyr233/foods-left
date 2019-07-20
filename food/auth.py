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
        user_phone= request.form['user_phone']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if user_phone == '123':
            error = 'Root is not availble.'
        elif not user_phone:
            error = 'User phone is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT user_phone FROM user WHERE user_phone = ?', (user_phone,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (user_phone, username, password, is_seller) VALUES (?, ?, ?, ?)',
                (user_phone, username, generate_password_hash(password), 0)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/store', methods=('GET', 'POST'))
def store():
    if request.method == 'POST':
        user_phone = request.form['user_phone']
        username = request.form['username']
        password = request.form['password']
        storename = request.form['storename']
        location = request.form['location']
        seller_intro = request.form['seller_intro']
        begintime = request.form['begintime']
        endtime = request.form['endtime']

        db = get_db()
        error = None

        if not user_phone:
            error = 'User phone is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT user_phone FROM user WHERE user_phone = ?', (user_phone,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (user_phone, username, password, is_seller) VALUES (?, ?, ?, ?)',
                (user_phone, username, generate_password_hash(password), 1)
            )
            db.commit()

            db.execute(
                'INSERT INTO seller (seller_phone, storename, seller_intro, location, begintime, endtime)'
                'VALUES (?, ?, ?, ?, ?, ?)', (user_phone, storename, seller_intro, location, begintime, endtime)
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
        user_phone = request.form['user_phone']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE user_phone = ?', (user_phone,)
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