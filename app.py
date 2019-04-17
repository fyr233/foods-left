import flask
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for

from random import randint
from datetime import timedelta

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=10)

@app.route('/')#主页
def index():
    if 'user' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('loginpage'))

@app.route('/login', methods = ['GET'])#登录页面
def loginpage():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])#登录请求
def loginpost():
    return redirect(url_for('index'))

@app.route('/mypage', methods = ['POST'])#‘我的’页面
def mypage():
    return render_template('mypage.html')

@app.route('/mypage/<path:path_name>', methods = ['POST'])#‘我的’下属页面/操作
def inmypage(path_name):

    if path_name == 'info':#‘我的’->基本信息与修改页面
        return render_template('mypage/info.html')

    if path_name == 'changebasicinfo':#‘我的’->修改基本信息提交
        return jsonify({'status':'OK'})

    if path_name[:6] == 'orders':

        if path_name == 'orders':#‘我的’->订单页面
            return render_template('mypage/orders.html')

        if path_name == 'orders/orderinfo':#‘我的’->订单->订单详情页面
            return render_template('mypage/orders/orderinfo.html')

        if path_name == 'orders/orderinfo/cancel':#‘我的’->订单->订单详情->取消订单请求
            return jsonify({'status':'OK'})

        if path_name == 'orders/orderinfo/comment':#‘我的’->订单->订单详情->提交评论
            return jsonify({'status':'OK'})
        
        if path_name == 'orders/orderinfo/rihgts':#‘我的’->订单->订单详情->提交维权信息
            return jsonify({'status':'OK'})

    if path_name == 'settings':#‘我的’->设置页面
        return render_template('mypage/settings.html')

    if path_name == 'changesettings':#‘我的’->修改设置提交
        return jsonify({'status':'OK'})

@app.route('/map', methods = ['POST'])#地图页面
def map():
    return render_template('map.html')

@app.route('/search', methods = ['POST'])#搜素结果页面，搜素参数在POSTdata中
def search():
    return render_template('search.html')

@app.route('/classify', methods = ['POST'])#分类页面
def classify():
    return render_template('classify.html')

@app.route('/classify/shoplist', methods = ['POST'])#商家列表查询，具体查询、排序方式在POSTdata中
def shoplist():
    return jsonify({'status':'OK'})

@app.route('/shop', methods = ['POST'])#商家主页
def shop():
    return render_template('shop.html')

@app.route('/shop/<path:path_name>', methods = ['POST'])#商家主页下属页面/操作
def inshop(path_name):

    if path_name == 'info':#商家主页->商家信息，如果用户是商家所有者，返回不同的html
        return render_template('shop/info.html')

    if path_name == 'foodlist':#商家主页->商家食品列表查询，参数在POSTdata中，店内搜索也使用此接口
        return jsonify({'status':'OK'})
    
    if path_name[:4] == 'food':

        if path_name == 'food':#商家主页->食品主页，包含图片、名称、余量、描述、日期、价格、评论等信息
            return render_template('shop/food.html')

        if path_name == 'food/share':#商家主页->食品主页->分享食品
            return jsonify({'status':'OK'})

        if path_name == 'food/report':#商家主页->食品主页->举报食品
            return jsonify({'status':'OK'})

        if path_name == 'food/add':#商家主页->食品主页->新增食品
            return jsonify({'status':'OK'})

        if path_name == 'food/del':#商家主页->食品主页->删除食品
            return jsonify({'status':'OK'})

        if path_name == 'food/change':#商家主页->食品主页->修改食品
            return jsonify({'status':'OK'})

    if path_name == 'follow':#商家主页->关注店铺
        return jsonify({'status':'OK'})

    if path_name == 'share':#商家主页->分享店铺
        return jsonify({'status':'OK'})

    if path_name == 'report':#商家主页->举报店铺
        return jsonify({'status':'OK'})

    if path_name == 'comment':#商家主页->评论店铺
        return jsonify({'status':'OK'})

    if path_name == 'changeinfo':#商家主页->修改商家信息
        return jsonify({'status':'OK'})

@app.route('/placeorder', methods = ['POST'])#下单页面
def placeorder():
    return render_template('placeorder.html')

@app.route('/placeorder/<path:path_name>', methods = ['POST'])#下单下属页面/操作
def inplaceorder(path_name):

    if path_name == 'cancel':#取消下单请求
        return jsonify({'status':'OK'})

    if path_name == 'pay':#付款请求
        return jsonify({'status':'OK'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)