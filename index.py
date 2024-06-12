from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for
from flask import session
from flask_bootstrap import Bootstrap
from flask_font_awesome import FontAwesome
import os
from flask_sqlalchemy import SQLAlchemy
# My Modules
from forms.login import LoginForm
from session.session import session_is_valid, session_destroy, session_start
from translator.translator import translate

load_dotenv()
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'thisismysecretkey'
app.config['locale'] = 'en_EN'
app.jinja_env.globals.update(translate=translate)
font_awesome = FontAwesome()
font_awesome.init_app(app)

# ALCHEMY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
path = 'sqlite:///{}/data.sqlite'.format(basedir)
app.config['SQLALCHEMY_DATABASE_URI'] = path
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session_is_valid():
        flash(translate('Your session has expired', session['locale'] if 'locale' in session else app.config['locale']))
        session_destroy()
        return redirect(url_for('login'))

    # Find and display lists for the given user
    title = translate('This is my page title', session['locale'])
    if 'started' not in session or not session['started']:
        flash(translate('Please log in', app.config['locale']))
        return redirect(url_for('login'))

    return render_template('index.html', title=title, locale=session['locale'])


@app.route('/logout')
def logout():
    session_destroy()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        from user.model import login, find_one_by_email
        if login(form.email.data, form.password.data):
            user = find_one_by_email(email=form.email.data)
            session_start(user, form.locale.data)
            flash(translate('Logged in successfully as {}', session['locale']).format(user.name))
            return redirect(url_for('index'))
        else:
            flash(translate('Wrong Email Or Password', app.config['locale']))
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
                           head=translate('404 Not Found',
                                          session['locale'] if 'locale' in session else app.config['locale']),
                           sub=str(e),
                           locale=session['locale'] if 'locale' in session else app.config['locale']), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html',
                           head=translate('500 Server Error',
                                          session['locale'] if 'locale' in session else app.config['locale']),
                           sub=str(e),
                           locale=session['locale'] if 'locale' in session else app.config['locale']), 500


if __name__ == "__main__":
    app.run()
