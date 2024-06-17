from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for
from flask import session
from flask_bootstrap import Bootstrap
from flask_font_awesome import FontAwesome

from forms.list import ListForm
from forms.list_item import ListItemForm
from forms.login import LoginForm
import list.model as ListModel
import list_item.model as ListItemModel
import session.session as Session
from translator.translator import translate
import os
from db import db

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
db.init_app(app)


def session_check():
    if not Session.session_is_valid():
        flash(translate('Your session has expired', session['locale'] if 'locale' in session else app.config['locale']))
        Session.session_destroy()
        return False

    if 'started' not in session or not session['started']:
        flash(translate('Please log in', app.config['locale']))
        return False

    return True


@app.route('/list_item_set_done/<item_list_id>/list_id/<list_id>', methods=['GET', 'POST'])
def list_item_set_done(item_list_id, list_id):
    Session.session_refresh()
    list = ListModel.list_find_by_id(list_id)
    list_item_set_done(item_list_id)
    flash(translate('Task {} done!', session['locale']).format(item_list_id))
    return redirect(url_for('list_display', list_id=list_id))


@app.route('/list_create', methods=['GET', 'POST'])
def list_create():
    Session.session_refresh()
    form = ListForm()
    if form.validate_on_submit():
        # create the list
        list_id = ListModel.list_create(form.name.data, session['user']['id'])
        return redirect(url_for('list_display', list_id=list_id))

    return render_template('list_create.html', form=form, locale=session['locale'])

@app.route('/list_item_fix_priorities/<list_id>')
def list_item_fix_priorities(list_id):
    Session.session_refresh()
    ListItemModel.list_item_fix_priorities(list_id)
    return redirect(url_for('list_display', list_id=list_id))

@app.route('/list_display/<list_id>', methods=['GET', 'POST'])
def list_display(list_id):
    Session.session_refresh()
    list = ListModel.list_find_by_id(list_id)
    items = ListItemModel.list_item_find_by_list_id(list_id)
    return render_template('list_display.html', items=items, list_id=list_id, list=list, locale=session['locale'])


@app.route('/list_edit/<list_id>', methods=['GET', 'POST'])
def list_edit(list_id):
    Session.session_refresh()
    list = ListModel.list_find_by_id(list_id)
    form = ListForm()

    if form.validate_on_submit():
        try:
            list.name = form.name.data
            db.session.commit()
            flash(translate("List '{}' renamed to '{}'", session['locale']).format(list_id, list.name))
            return redirect(url_for('index'))
        except Exception as e:
            return server_error(e)

    # Populate the name field in the form
    form.name.data = list.name
    return render_template('list_edit.html', form=form, list_id=list_id)


@app.route('/list_delete/<list_id>', methods=['GET', 'POST'])
def list_delete(list_id):
    Session.session_refresh()
    list_delete(list_id)
    return redirect(url_for('index'))


@app.route('/list_item_create/<list_id>', methods=['GET', 'POST'])
def list_item_create(list_id):
    Session.session_refresh()
    list = ListModel.list_find_by_id(list_id)
    form = ListItemForm()
    if form.validate_on_submit():
        # create the item
        ListItemModel.list_item_create(list_id, form.text.data, form.prio.data)
        return redirect(url_for('list_display', list_id=list_id))
    title = translate('New Task In List {}'.format(list_id), session['locale'])
    return render_template('list_item_create.html', list=list, form=form, title=title, locale=session['locale'])


@app.route('/', methods=['GET', 'POST'])
def index():
    Session.session_refresh()
    title = translate('Hello, {}'.format(session['user']['name']), session['locale'])
    if not session_check():
        return redirect(url_for('login'))
    # Find and display lists for the given user
    app.jinja_env.globals.update(list_get_item_count=ListItemModel.list_get_item_count)
    return render_template('index.html', title=title, locale=session['locale'],
                           lists=ListModel.list_find_by_user_id(session['user']['id']))


@app.route('/logout')
def logout():
    Session.session_destroy()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        from user.model import user_login, user_find_one_by_email
        if user_login(form.email.data, form.password.data):
            user = user_find_one_by_email(email=form.email.data)
            Session.session_start(user, form.locale.data)
            flash(translate('Logged in successfully as {}', session['locale']).format(user.name))
            return redirect(url_for('index'))
        else:
            flash(translate('Wrong Email Or Password', app.config['locale']))
            return redirect(url_for('login'))

    return render_template('login.html', form=form, locale=app.config['locale'])


@app.errorhandler(404)
def page_not_found(e):
    Session.session_refresh()
    return render_template('404.html',
                           head=translate('404 Not Found',
                                          session['locale'] if 'locale' in session else app.config['locale']),
                           sub=str(e),
                           locale=session['locale'] if 'locale' in session else app.config['locale']), 404


@app.errorhandler(500)
def server_error(e):
    Session.session_refresh()
    return render_template('500.html',
                           head=translate('500 Server Error',
                                          session['locale'] if 'locale' in session else app.config['locale']),
                           sub=str(e),
                           locale=session['locale'] if 'locale' in session else app.config['locale']), 500


if __name__ == "__main__":
    app.run()
