# $ pip install --upgrade -r requirements.txt
# $ python -m flask run

from flask import Flask, render_template, request
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp


application = Flask(__name__)

application.config['TEMPLATES_AUTO_RELOAD'] = True
application.secret_key = 'development key'


@application.route('/')
def index():
    return render_template('index.html')

@application.route('/enter_pin')
def booth_enter_pin():
    return render_template('enter_pin.html')

@application.route('/cast_vote')
def booth_cast_vote():
    return render_template('cast_vote.html')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
