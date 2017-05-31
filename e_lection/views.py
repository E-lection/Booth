from e_lection import app
from flask import render_template
from flask import request

from forms import FindVoterForm

@app.route('/')
def index():
    return render_template('index.html')

################## STATION STUFF ##################

# @app.route('/station')
# def station():
#     return render_template('station.html')
#
# @app.route('/station', methods=['POST'])
# def find_voter():
#     form = FindVoterForm()
#     if form.validate_on_submit():
#         return render_template('voterdb.html', form = form)
#     return render_template('station.html', form = form)

#################################################

################## BOOTH STUFF ##################

@app.route('/booth_enter_pin')
def booth_enter_pin():
    return render_template('booth_enter_pin.html')

@app.route('/booth_cast_vote')
def booth_cast_vote():
    return render_template('booth_cast_vote.html')

#################################################
