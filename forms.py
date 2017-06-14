from flask_wtf import FlaskForm as Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp
PIN_REGEX = '^[0-9][0-9][0-9][0-9][0-9][0-9]$'
class LoginForm(Form):
    username = StringField('username', validators=[])
    password = StringField('password', validators=[])

class PinForm(Form):
    voterpin = StringField('voterpin')
    voterpin = StringField('voterpin', validators=[DataRequired("Error! No pin entered."),
    Regexp(PIN_REGEX, message="Error! Invalid PIN.")])
