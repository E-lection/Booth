# $ pip install --upgrade -r requirements.txt
# $ python -m flask run

from flask import Flask, render_template, request, redirect
from flask_wtf import Form
from forms import LoginForm
from forms import PinForm
from wtforms import StringField
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
import flask_login
import urllib, urllib2
import json
import models as db
from passlib.apps import custom_app_context as pwd_context

application = Flask(__name__)

application.config['TEMPLATES_AUTO_RELOAD'] = True
application.secret_key = 'development key'
candidates_json = None
voter_active = False

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

@application.route('/login', methods=['GET', 'POST'])
def login():
    global candidates_json
    if request.method == 'POST':
        form = LoginForm(request.form)
        username = request.form['username']
        password = request.form['password']
        valid_user = get_valid_user(username, password)
        if valid_user:
            user = User(valid_user[0], username, valid_user[1])
            login_user(user)
            # Get list of candidates on startup
            # TODO: check for exception
            return redirect('')
        else:
            return render_template('login.html', message="Login unsuccessful.", form=form)
    else:
        form = LoginForm(request.form)
        return render_template('login.html', form=form)

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
    form = PinForm(request.form)
    return render_template('enter_pin.html', form=form)

@application.route('/', methods=['POST'])
@login_required
def verify_pin():
    global voter_active
    form = PinForm(request.form)
    if form.validate_on_submit():
        pin = request.form['voterpin']
        url = createPapiURL(pin)
        try:
            dbresult = urllib2.urlopen(url).read()
        except:
            return render_template('enter_pin.html', message="Inavlid Request", form=form)
        resultjson = json.loads(dbresult)
        success = resultjson['success']
        if success:
            # matching entry found
            voted = False
            if voted:
                return render_template('enter_pin.html', message="You've already voted. PIN already used", form=form)
            else:
                voter_active = True
                print ('assigning voter_active to TRUE')
                return redirect('/cast_vote')
        else:
            # no matching entry in database, try again
            return render_template('enter_pin.html', message="Invalid Voter PIN", form=form)

    return render_template('enter_pin.html', form=form)

@application.route('/cast_vote', methods=['GET'])
@login_required
def choose_candidate():
    global candidates_json
    global voter_active
    if voter_active:
        if not candidates_json:
            updateCandidatesJson()
        return render_template('cast_vote.html', candidates=candidates_json['candidates'])
    else:
        # Voter not logged in
        return redirect('')

@application.route('/cast_vote', methods=['POST'])
@login_required
def cast_vote():
    global voter_active
    voter_active = False
    return render_template('cast_vote.html')

def createPapiURL(pin):
    station_id = "/station_id/" + urllib.quote(str(flask_login.current_user.station_id))
    pin = "/pin_code/" + urllib.quote(pin)
    url = "http://pins.eelection.co.uk/verify_pin_code"+station_id+pin
    return url

def createCandidatesURL():
    station_id = "/" + urllib.quote(str(flask_login.current_user.station_id))
    url = "http://voting.eelection.co.uk/get_candidates"+station_id
    return url

def updateCandidatesJson():
    global candidates_json
    dbresult = urllib2.urlopen(createCandidatesURL()).read()
    resultjson = json.loads(dbresult)
    candidates_json = resultjson

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
