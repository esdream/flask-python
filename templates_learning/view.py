from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    mydict = { 'key': 'Lucio' }
    mylist = [324, 'sdf', True, (2, 4)]
    return render_template('user.html', name=name, mylist=mylist, mydict=mydict)

if(__name__ == '__main__'):
    app.run(debug=True)
