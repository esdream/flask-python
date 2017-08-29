from flask import Flask
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/')
def index():
    print(app.config)
    return ''

if(__name__ == '__main__'):
    app.run(debug=True)
