# $ pip install --upgrade -r requirements.txt
# $ python -m flask run

from flask import Flask
app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'development key'

import e_lection.views
import e_lection.forms
