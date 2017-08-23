from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    # mydict = { 'key': 'Lucio' }
    # mylist = [324, 'sdf', True, (2, 4)]
    return render_template('user_bootstrap.html', name=name)

if(__name__ == '__main__'):
    app.run(debug=True)
