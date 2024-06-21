import os
from app import create_app, db
from flask_migrate import Migrate
from list import model as list_model
from user import model as user_model
from list_item import model as list_item_model

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, list_model=list_model, user_model=user_model, list_item_model=list_item_model)
