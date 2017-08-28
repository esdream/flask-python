from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    # mydict = { 'key': 'Lucio' }
    # mylist = [324, 'sdf', True, (2, 4)]
    return render_template('user_bootstrap.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.thml'), 500

@app.route('/test')
def test_url_for():
    print(url_for('user', name='letian'))
    print(url_for('index'))
    print(url_for('user', name='join', _external=True))
    print(url_for('index', raper=3))
    print(url_for('static', filename='css/style.css', _external=True))
    # 视图函数必须要有返回值
    return ''

if(__name__ == '__main__'):
    app.run(debug=True)
