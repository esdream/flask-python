from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import Form
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
    if(form.validate_on_submit()):
        # name = form.name.data
        old_name = session.get('name')
        if(old_name is not None and old_name != form.name.data):
            flash('You have changed your name!')
        session['name'] = form.name.data
        # form.name.data = ''
        # print(name)
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

if(__name__ == '__main__'):
    app.run(debug=True)
