
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
#toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register' , methods=['GET' , 'POST'])
def show_register_form():
    """Show register form and process the register form by adding a new user"""
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username,password,email,first_name,last_name)

        db.session.commit()
        session['username'] = user.username

        return redirect('/secret')
    
    else: 
        return render_template('register.html' , form=form)

@app.route('/login' , methods=['GET' , 'POST'])
def login_form():
    """ Show and process loginform"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username.password)
        session['username'] = user.username
    #we’re going to make sure that when we log a user in (and after they register), 
    #we store just a little information in the session. When the user successfully registers or logs in, store the username in the session.
        return redirect('/secret')

@app.route('/users/<username>')
def show_user(username):
    """Display a template the shows information about that user """
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("details.html", user=user, form=form)

@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")
#Clear any information from the session and redirect to /


