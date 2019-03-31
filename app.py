import flask
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from random import randint

from datetime import timedelta

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=10)

@app.route('/')
@app.route('/login')
def indexpage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)