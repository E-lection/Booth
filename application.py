# $ pip install --upgrade -r requirements.txt
# $ python -m flask run

from flask import Flask, render_template, request, redirect
from flask_wtf import Form
from forms import LoginForm
from wtforms import StringField
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
import models as db
from passlib.apps import custom_app_context as pwd_context

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

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        username = request.form['username']
        password = request.form['password']
        valid_user = get_valid_user(username, password)
        if valid_user:
            user = User(valid_user[0], username, valid_user[1])
            login_user(user)
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
        return User(user[0], user[1], user[2])
    else:
        return None

# Once logged in successfully, use booth app to vote
@application.route('/', methods=['GET'])
@login_required
def station():
    return render_template('enter_pin.html')

@application.route('/cast_vote')
@login_required
def booth_cast_vote():
    return render_template('cast_vote.html')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
