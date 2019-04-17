from flask import Flask, session, redirect, url_for, escape, request, render_template
from datetime import datetime

app = Flask(__name__)

#Secret key
app.secret_key = 'z4hvb\JSĸ9LIE'

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username='Logged in as %s' % escape(session['username']))
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] == 'admin') & (request.form['password'] == 'password'):
            session['username'] = request.form['username']
            return render_template('index.html', username='Logged in as %s' % escape(session['username']))
        else:
            error = 'Invalid username/password'
            return render_template('login.html', error=error)
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
