from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from translator.translator import translate


class ListForm(FlaskForm):
    name = StringField(translate('Name'), validators=[DataRequired()])
    submit = SubmitField(translate('Save'))
