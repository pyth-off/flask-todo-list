from flask import flash, redirect, url_for, render_template, session

from db import db
from forms.list import ListForm
from forms.list_item import ListItemForm
from forms.login import LoginForm
import list.model as list_model
import list_item.model as list_item_model
from session import session as s
from session.session import destroy, start
from translator.translator import translate
from . import main
from .errors import server_error


def session_check():
    if not s.is_valid():
        flash(translate('Your session has expired', session['APP_LOCALE'] if 'APP_LOCALE' in session else main.config['APP_LOCALE']))
        s.destroy()
        return False

    if 'started' not in session or not session['started']:
        flash(translate('Please log in', main.config['APP_LOCALE']))
        return False

    return True


@main.route('/list_item_set_done/<item_list_id>/list_id/<list_id>', methods=['GET', 'POST'])
def list_item_set_done(item_list_id, list_id):
    s.refresh()
    list = list_model.find_by_id(list_id)
    list_item_model.set_done(item_list_id)
    flash(translate('Task {} done!', session['APP_LOCALE']).format(item_list_id))
    return redirect(url_for('.list_display', list_id=list_id))


@main.route('/list_create', methods=['GET', 'POST'])
def list_create():
    s.refresh()
    form = ListForm()
    if form.validate_on_submit():
        # create the list
        list_id = list_model.create(form.name.data, session['user']['id'])
        return redirect(url_for('.list_display', list_id=list_id))

    return render_template('list_create.html', form=form, locale=session['APP_LOCALE'])


@main.route('/list_item_fix_priorities/<list_id>')
def list_item_fix_priorities(list_id):
    s.refresh()
    list_item_model.reset_priorities(list_id)
    return redirect(url_for('.list_display', list_id=list_id))


@main.route('/list_display/<list_id>', methods=['GET', 'POST'])
def list_display(list_id):
    s.refresh()
    list = list_model.find_by_id(list_id)
    items = list_item_model.find_by_list_id(list_id)
    return render_template('list_display.html', items=items, list_id=list_id, list=list, locale=session['APP_LOCALE'])


@main.route('/list_edit/<list_id>', methods=['GET', 'POST'])
def list_edit(list_id):
    s.refresh()
    list = list_model.find_by_id(list_id)
    form = ListForm()

    if form.validate_on_submit():
        try:
            list.name = form.name.data
            db.session.commit()
            flash(translate("List '{}' renamed to '{}'", session['APP_LOCALE']).format(list_id, list.name))
            return redirect(url_for('.index'))
        except Exception as e:
            return server_error(e)

    # Populate the name field in the form
    form.name.data = list.name
    return render_template('list_edit.html', form=form, list_id=list_id)


@main.route('/list_delete/<list_id>', methods=['GET', 'POST'])
def list_delete(list_id):
    s.refresh()
    list_model.delete(list_id)
    return redirect(url_for('.index'))


@main.route('/list_item_create/<list_id>', methods=['GET', 'POST'])
def list_item_create(list_id):
    s.refresh()
    list = list_model.find_by_id(list_id)
    form = ListItemForm()
    if form.validate_on_submit():
        # create the item
        list_item_model.create(list_id, form.text.data, form.prio.data)
        return redirect(url_for('main.list_display', list_id=list_id))

    title = translate('New Task In List {}'.format(list_id), session['APP_LOCALE'])
    return render_template('list_item_create.html', list=list, form=form, title=title, locale=session['APP_LOCALE'])


@main.route('/', methods=['GET', 'POST'])
def index():
    s.refresh()
    title = translate('Hello, {}'.format(session['user']['name']), session['APP_LOCALE'])
    if not session_check():
        return redirect(url_for('.login'))
    return render_template('index.html', title=title, locale=session['APP_LOCALE'],
                           lists=list_model.find_by_user_id(session['user']['id']))


@main.route('/logout')
def logout():
    s.destroy()
    return redirect(url_for('.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        from user.model import login, find_by_email
        if login(form.email.data, form.password.data):
            user = find_by_email(email=form.email.data)
            s.start(user, form.locale.data)
            flash(translate('Logged in successfully as {}', session['APP_LOCALE']).format(user.name))
            return redirect(url_for('.index'))
        else:
            flash(translate('Wrong Email Or Password', main.config.APP_LOCALE))
            return redirect(url_for('.login'))

    return render_template('login.html', form=form, locale=main.config.APP_LOCALE)
