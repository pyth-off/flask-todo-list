from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField
from wtforms.validators import DataRequired
from translator.translator import translate


class ListItemForm(FlaskForm):
    text = StringField(translate('Task'), validators=[DataRequired()])
    prio = IntegerField(translate('Priority'), default=10,validators=[DataRequired()])
    submit = SubmitField(translate('Save'))