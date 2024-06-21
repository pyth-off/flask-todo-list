from flask import render_template, session

from session.session import refresh
from translator.translator import translate
from . import main


@main.errorhandler(404)
def page_not_found(e):
    refresh()
    return render_template('404.html',
                           head=translate('404 Not Found',
                                          session['APP_LOCALE'] if 'APP_LOCALE' in session else main.config['APP_LOCALE']),
                           sub=str(e),
                           locale=session['APP_LOCALE'] if 'APP_LOCALE' in session else main.config['APP_LOCALE']), 404


@main.errorhandler(500)
def server_error(e):
    refresh()
    return render_template('500.html',
                           head=translate('500 Server Error',
                                          session['APP_LOCALE'] if 'APP_LOCALE' in session else main.config['APP_LOCALE']),
                           sub=str(e),
                           locale=session['APP_LOCALE'] if 'APP_LOCALE' in session else main.config['APP_LOCALE']), 500
