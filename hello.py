from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'thisismysecretkey'


@app.route('/')
def index():
    return render_template('index.html')


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Register this view function as a handler for GET and POST requests
@app.route('/form', methods=['GET', 'POST'])
def form():
    # Init variables
    name = None
    form = NameForm()
    # The form is ok
    if form.validate_on_submit():
        name = form.name.data
        flash('Data received!')
    return render_template('form.html', form=form, name=name)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
