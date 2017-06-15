# $ pip install --upgrade -r requirements.txt
# $ python -m flask run

from api_key_verification import BOOTH_KEY
from flask import Flask, render_template, request, redirect, session
from flask_wtf import FlaskForm as Form
from forms import LoginForm
from forms import PinForm
from wtforms import StringField
import flask_login
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
import urllib, urllib2
import json
import models as db
from passlib.apps import custom_app_context as pwd_context
import requests

application = Flask(__name__)

application.config['TEMPLATES_AUTO_RELOAD'] = True
application.secret_key = 'development key'

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "login"

# Booth User model
class User(UserMixin):
    def __init__(self, id, username, station_id):
        self.id = id
        self.station_id = station_id
        self.username = username

    def __repr__(self):
        return "%s/%d" % (self.username, self.station_id)

# Displays login page for the clerk to set up the booth
@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    # If someone has tried to log in
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        valid_user = get_valid_user(username, password)
        if valid_user:
            user = User(valid_user[0], username, valid_user[1])
            login_user(user)
            session['candidates_json'] = None
            session['voter_active'] = False
            session['voted_candidate'] = None
            session['vote_sent'] = False
            return redirect('')
        else:
            return render_template('login.html', message="Login unsuccessful.", form=form)
    return render_template('login.html', form=form)

# Checks user user_id and station_id for that usename and password
def get_valid_user(username, password):
    users = db.retrieveUsers()
    user_id = -1
    station_id = -1
    for user in users:
        if user[1] == username:
            password_hash = user[2]
            if pwd_context.verify(password, password_hash):
                user_id = user[0]
                station_id = user[3]
                return (user_id, station_id)
            break
    #TODO: Error if there is no user matching
    return None


@application.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


# handle login failed
@application.errorhandler(401)
def page_not_found(e):
    return render_template('login.html', message="Login unsuccessful.", form=form)


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    users = db.retrieveUsers()
    users_with_id = filter(lambda x: x[0] == int(userid), users)
    if users_with_id:
        user = users_with_id[0]
        return User(user[0], user[1], user[3])
    else:
        return None

# Once logged in successfully, use booth app to vote
@application.route('/', methods=['GET'])
@login_required
def enter_pin():
    if session['voter_active']:
        return redirect('/cast-vote')
    form = PinForm(request.form)
    return render_template('enter_pin.html', form=form, not_banner=True)

@application.route('/', methods=['POST'])
@login_required
def verify_pin():
    if session['voter_active']:
        return redirect('/cast-vote')

    form = PinForm(request.form)
    if form.validate_on_submit():
        pin = request.form['voterpin']
        session['voterpin'] = pin
        papiResponse = getPapiResponse(pin)
        success = papiResponse['valid_pin']
        if success:
            # matching entry found
            voted = papiResponse['already_voted']
            if voted:
                return render_template('enter_pin.html', message="You've already voted. PIN already used", form=form)
            else:
                session['voter_active'] = True
                session['vote_sent'] = False
                session['candidates_json'] = None
                session['voting_error'] = None
                return redirect('/cast-vote')
        else:
            # no matching entry in database, try again
            return render_template('enter_pin.html', message="Invalid Voter PIN", form=form)

    return render_template('enter_pin.html', message="Invalid voter pin entered", form=form)

# Checks if the voter is logged in and loads candidate options
@application.route('/cast-vote', methods=['GET'])
@login_required
def choose_candidate():
    if not session['voter_active']:
        return redirect('')
    else:
        if not session['candidates_json']:
            session['candidates_json'] = getCandidatesJson()
            if len(session['candidates_json']['candidates']) == 0:
                session['voter_active'] = False
                form = PinForm(request.form)
                return render_template('enter_pin.html', message="No running candidates found for this constituency.", form=form)
        return render_template('cast_vote.html', candidates=session['candidates_json']['candidates'])

@application.route('/cast-vote', methods=['POST'])
@login_required
def cast_vote():
    if session['voter_active']:
        candidate_id = int(request.json['candidate_id'])
        if not candidate_id:
            session['voted_candidate'] = 'SPOILT'
        else:
            session['voted_candidate'] = getCandidateWithPK(candidate_id, session['candidates_json']['candidates'])
        return 'OK'
    else:
        return redirect('')

@application.route('/confirm-vote', methods=['GET'])
@login_required
def show_candidate():
    if session['voter_active'] and session['voted_candidate']:
        return render_template('confirm_vote.html', candidate=session['voted_candidate'])
    else:
        return redirect('')

@application.route('/confirm-vote', methods=['POST'])
@login_required
def confirm_vote():
    confirm = int(request.json['confirm'])
    if confirm and session['voter_active'] and session['voted_candidate']:
        # TODO: What do we send in case of spoilt ballot
        if 'voterpin' in session:
            session['voted_candidate']['pin_code'] = session['voterpin']
            session['voted_candidate']['station_id'] = flask_login.current_user.station_id
            resultsResp = sendVote(session['voted_candidate'])
            if resultsResp:
                if resultsResp['success']:
                    # Voting successful
                    session['vote_sent'] = True
                else:
                    session['voting_error'] = resultsResp['error']
                session['voter_active'] = False
                session['voted_candidate'] = None
            # else:
        # else:
        return 'OK'
    else:
        return redirect('')

@application.route('/youve-voted')
@login_required
def youve_voted():
    if session['voting_error']:
        session['voting_error'] = None
        form = PinForm(request.form)
        return render_template('enter_pin.html', message="Voter pin already used.", form=form)
    # Voting unsuccessful, retry (should redirect to enter pin?), we have the voted_candidate with us though
    if session['voter_active'] and session['voted_candidate'] and (not session['vote_sent']):
        return redirect('/cast-vote')
    session['vote_sent'] = False
    return render_template('youve_voted.html')

# Gets PAPI resposne for a voter pin
def getPapiResponse(pin):
    station_id = "/station_id/" + urllib.quote(str(flask_login.current_user.station_id))
    pin = "/pin_code/" + urllib.quote(pin)
    url = "http://pins.eelection.co.uk/verify_pin_code_and_check_eligibility"+station_id+pin
    print url
    try:
        request = urllib2.Request(url)
        request.add_header("Authorization", BOOTH_KEY)
        dbresult = urllib2.urlopen(request).read()
    except:
        return None
    return json.loads(dbresult)

# Gets the list of candidates for that station
def createCandidatesURL():
    station_id = "/" + urllib.quote(str(flask_login.current_user.station_id))
    url = "http://voting.eelection.co.uk/get_candidates"+station_id
    return url

# Sets candidates_json to the correct stuff for that station
def getCandidatesJson():
    request = urllib2.Request(createCandidatesURL())
    request.add_header("Authorization", BOOTH_KEY);
    dbresult = urllib2.urlopen(request).read()
    resultjson = json.loads(dbresult)
    return resultjson

def sendVote(voted_candidate):
    url = "http://results.eelection.co.uk/vote/"
    response = requests.post(url=url, data=json.dumps(voted_candidate),
                        headers={'Authorization': BOOTH_KEY})
    if response.status_code==200:
        print "sent vote"
        resultJson = json.loads(response.text)
        return resultJson
    else:
        # Coudn't contact results server
        return None

def getCandidateWithPK(pk, candidates):
    global candidates_json
    for candidate in candidates:
        if candidate['pk'] == pk:
            return candidate['fields']
    return None
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
