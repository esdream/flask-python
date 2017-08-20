from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    mydict = { 'key': 65535 }
    mylist = [3, 4, 5, 6]
    print(mydict['key'])
    return render_template('user.html', name=name, mydict=mydict)

if(__name__ == '__main__'):
    app.run(debug=True)
