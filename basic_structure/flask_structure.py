from flask import Flask, request, make_response, redirect, abort
from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

@app.route('/redir')
def redir():
    return redirect('http://www.google.com')

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

@app.route('/num/<int:id>')
def num(id):
    user = load_user(id)
    # if not suer:
    #     abort(404)
    return '<h1>Your id is %d</h1>' % id


if(__name__) == '__main__':
    manager.run()
