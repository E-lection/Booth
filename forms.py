from flask_wtf import Form
from wtforms import StringField

class LoginForm(Form):
    username = StringField('username', validators=[])
    password = StringField('password', validators=[])
