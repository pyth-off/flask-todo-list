from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email
from translator.translator import translate


class LoginForm(FlaskForm):
    email = StringField(translate('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(translate('Password'), validators=[DataRequired()])
    choices = {'en_EN': 'English', 'de_DE': 'Deutsch'}
    locale = SelectField(translate('Locale'), choices=[choice for choice in choices])
    submit = SubmitField(translate('Login'))
