from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

class FindVoterForm(Form):
    firstname = StringField('firstname', validators=[DataRequired("No name entered."),
    Regexp('/^[a-z ,.\'-]+$/i', message="Invalid first name entered")])
    postcode = StringField('password', validators=[DataRequired("No postcode entered."),
    Regexp('(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2})', message="Invalid postcode entered")])
