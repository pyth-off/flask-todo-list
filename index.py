import datetime

from flask import Flask, render_template, flash, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_font_awesome import FontAwesome
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email
import time

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'thisismysecretkey'

font_awesome = FontAwesome()
font_awesome.init_app(app)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/')
def index():
    title = 'This is my page title'
    if 'started' not in session or not session['started']:
        flash('Please log in')
        return redirect(url_for('login'))

    return render_template('index.html', title=title)

@app.route('/logout')
def logout():
    session['started'] = False
    session['start'] = None
    session['email'] = None
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'czarito@web.de' and form.password.data == '1234':
            session['started'] = True
            session['start'] = time.time()
            session['email'] = form.email.data
            flash("Logged in successfully as {}".format(form.email.data))
            return redirect(url_for('index'))
        else:
            flash('Wrong email or password')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', head='404 Not Found', sub=str(e)), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html', head='500 Server Error', sub=str(e)), 500


if __name__ == "__main__":
    app.run()
