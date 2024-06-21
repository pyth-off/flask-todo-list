from config import config
from db import db
from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for
from flask import session
from flask_bootstrap import Bootstrap
from flask_font_awesome import FontAwesome
from forms.list import ListForm
from forms.list_item import ListItemForm
from forms.login import LoginForm
from translator.translator import translate
import list.model as list_model
import list_item.model as list_item_model
import os
import session.session as Session

bootstrap = Bootstrap()
font_awesome = FontAwesome()


def create_app(config_name):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.jinja_env.globals.update(translate=translate)
    app.jinja_env.globals.update(list_get_item_count=list_item_model.get_item_count)

    bootstrap.init_app(app)
    db.init_app(app)
    font_awesome.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    main_blueprint.config = config[config_name]
    return app



