from flask_wtf import FlaskForm as Form
from wtforms import StringField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('username', validators=[])
    password = StringField('password', validators=[])

class PinForm(Form):
    voterpin = StringField('voterpin')
