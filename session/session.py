from flask import session
import time

"""Session related functions"""


def is_valid():
    """Checks for session validity and expiration time"""
    if 'start' not in session or not session['start'] or (time.time() - session['start']) >= 600:
        return False
    return True


def refresh():
    session['start'] = time.time()


def start(user, locale):
    """Starts session"""
    session['started'] = True
    session['start'] = time.time()
    session['user'] = {}
    session['user']['id'] = user.id
    session['user']['name'] = user.name
    session['user']['email'] = user.email
    session['APP_LOCALE'] = locale
    return True


def destroy():
    """Destroys the active session"""
    if 'started' in session:
        session.pop('started', None)
    if 'user' in session:
        session.pop('user', None)
    if 'start' in session:
        session.pop('start', None)
    if 'APP_LOCALE' in session:
        session.pop('APP_LOCALE', None)
