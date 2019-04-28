from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from food.auth import login_required
from food.db import get_db
import random

import datetime
bp = Blueprint('products', __name__)


@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        'SELECT p.product_create, p.productname, p.price, p.type, p.producetime, p.qualitytime, s.seller_phone, s.storename'
        ' FROM product p JOIN seller s ON p.seller_phone = s.seller_phone'
        ' ORDER BY p.product_create DESC'
    ).fetchall()
    return render_template('index.html', products=products)

'''商家新建商品'''
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        qualitytime = request.form['qualitytime']
        producetime = request.form['producetime']
        type = request.form['type']
        productname = request.form['productname']
        price = request.form['price']
        error = None
        product_create = random.randint(1, 10000000);

        if not productname:
            error = 'Product name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (product_create, seller_phone, producetime, qualitytime, type, productname, price)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (product_create, g.user['user_phone'], producetime, qualitytime, type, productname, price)
            )
            db.commit()
            return redirect(url_for('products.index'))

    return render_template('products/create.html')

def get_products(id, check_author=True):
    product = get_db().execute(
        'SELECT p.product_create, productname, price, type, producetime, qualitytime, seller_id'
        ' FROM product p JOIN seller s ON p.seller_phone = s.seller_phone'
        ' WHERE p.seller_phone = ?',
        (id,)
    ).fetchone()

    if product is None:
        abort(404, "Product id {0} doesn't exist.".format(id))

    if check_author and product['seller_phone'] != g.user['user_phone']:
        abort(403)

    return product

'''商家更新商品信息'''
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    product = get_products(id)

    if request.method == 'POST':
        qualitytime = request.form['qualitytime']
        producetime = request.form['producetime']
        type = request.form['type']
        productname = request.form['productname']
        price = request.form['price']
        error = None

        if not productname:
            error = 'Product name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE product SET productname = ?, producetime = ?, qualitytime = ?, type = ?, price = ?'
                ' WHERE product_create = ?',
                (productname, producetime, qualitytime, type, price, id)
            )
            db.commit()
            return redirect(url_for('products.index'))

    return render_template('products/update.html', product=product)

'''商家删除商品'''
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_products(id)
    db = get_db()
    db.execute('DELETE FROM product WHERE product_create = ?', (id,))
    db.commit()
    return redirect(url_for('products.index'))


'''顾客订购'''
@bp.route('/trade', methods=('GET', 'POST'))
@login_required
def trade(id, trade_number):
    product = get_products(id)
    nowtime = datetime.datetime.now()

    db = get_db()
    db.execute(
        'INSERT INTO trade (product_create, user_phone, seller_phone, trade_time, cancel, trade_number)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (id, g.user['user_phone'], product['productname'], nowtime, 0, trade_number)
    )
    db.commit()
    return redirect(url_for('products.index'))