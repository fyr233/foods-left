from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from food.auth import login_required
from food.db import get_db
import random
import pyqrcode
import os

import datetime
bp = Blueprint('products', __name__)


@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        'SELECT p.product_create, p.productname, p.price, p.type, p.producetime, p.qualitytime, s.seller_phone, s.storename'
        ' FROM product p JOIN seller s ON p.seller_phone = s.seller_phone'
        ' ORDER BY p.producetime DESC'
    ).fetchall()
    return render_template('index.html', products=products)


'''显示地图'''
@bp.route('/my')
def map():
    return render_template('my.html')

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
        product_create = random.randint(1, 3);

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
        'SELECT p.product_create, productname, price, type, producetime, qualitytime, s.seller_phone'
        ' FROM product p JOIN seller s ON p.seller_phone = s.seller_phone'
        ' WHERE p.product_create = ?',
        (id,)
    ).fetchone()

    if product is None:
        abort(404, "Product id {0} doesn't exist.".format(id))


    print("???")
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

    return render_template('products/update.html')

'''商家删除商品'''
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_products(id)
    db = get_db()
    db.execute('DELETE FROM product WHERE product_create = ?', (id,))
    db.commit()
    return redirect(url_for('products.index'))

'''订单'''
@bp.route('/list')
@login_required
def list():
    db = get_db()
    products = db.execute(
        'SELECT p.product_create, p.productname, p.price, p.type, p.producetime, p.qualitytime, s.seller_phone, s.storename, t.trade_time , t.cancel , t.user_phone FROM product p ,seller s , trade t'
        ' WHERE p.seller_phone = s.seller_phone AND t.product_create = p.product_create'
        ' AND (t.user_phone = ? OR t.seller_phone = ?)'
        'ORDER BY t.trade_time DESC',
        (g.user['user_phone'], g.user['user_phone'])
    )
    db.commit()
    return render_template('products/trade.html', products=products)

'''顾客订购'''
@bp.route('/<int:id>/trade', methods=('GET', 'POST'))
@login_required
def trade(id):

    product = get_products(id)
    nowtime = datetime.datetime.now()

    #print(os.getcwd())
    qr = pyqrcode.create(str(id))
    qr.svg("static/image/qrcodes/"+str(id)+"-qrcode.svg", scale=8)#没写完#现在写完了

    db = get_db()
    db.execute(
        'INSERT INTO trade (product_create, user_phone, seller_phone, trade_time, cancel, trade_number)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (id, g.user['user_phone'], product['seller_phone'], nowtime, 0, 1)
    )
    db.commit()
    return redirect(url_for('products.list'))

'''商家发货'''
@bp.route('/<int:id>/send', methods=('GET', 'POST'))
@login_required
def send(id):

    db = get_db()
    db.execute(
        ' UPDATE trade SET cancel = 1 WHERE product_create = ?',
        (id,)
    )
    db.commit()
    return redirect(url_for('products.list'))


'''顾客收货'''
@bp.route('/<int:id>/receive', methods=('GET', 'POST'))
@login_required
def receive(id):
    db = get_db()
    db.execute(
        ' UPDATE trade SET cancel = 2 WHERE product_create = ?',
        (id, )
    )
    db.commit()
    return redirect(url_for('products.list'))

'''删除订单'''
@bp.route('/<int:id>/orderdelete', methods=('POST',))
@login_required
def orderdelete(id):
    get_products(id)
    db = get_db()
    db.execute('DELETE FROM trade WHERE product_create = ?', (id,))
    db.commit()
    return redirect(url_for('products.index'))
