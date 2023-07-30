from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc1knmlo23"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
#toolbar = DebugToolbarExtension(app) -- causes error everytime it runs

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register' , methods=['GET' , 'POST'])
def register_form():
    """ Show the register form and process the registration form by adding a new user """
    
    form = RegisterForm()   #in the form.py

    if form.validate_on_submit():    #getting all the data from the form
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username,password,email,first_name,last_name)

        db.session.commit()
        session['username'] = user.username

        return redirect(f'/users/{user.username}') ####??????
    
    else: 
        return render_template('register.html' , form=form)

#### Didn't get this route ####
@app.route('/login' , methods=['GET' , 'POST'])
def login_form():
    """ Show and process loginform """

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm() #the loginform from forms.py

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password) 
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)
       
    return render_template("login.html", form=form)
        
       

@app.route('/users/<username>')
def show_user(username):
    """Display a template that shows information about that user """
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    #to make sure that only logged-in users can access this page

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("details.html", user=user , form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """ Remove the user from the database and delete all of their feedback"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
        #only the user who is logged in can successfully delete their account

    user = User.query.get(username) #get the user having a specific username
    db.session.delete(user) #delete user from the database
    db.session.commit()

    session.pop("username") #clear user information from the session

    return redirect("/login")

@app.route("/users/<username>/feedback/add" , methods=["GET" , "POST"])
def add_feedback(username):
    """Add feedback"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title , content=content , username=username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("add_feedback.html" , form=form)


@app.route("/feedback/<int:feedback_id>/update" , methods=["GET" , "POST"])
def update_feedback(feedback_id):
    """Update a specific piece of feedback"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj = feedback) ####?????????????

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect(f'/users/{feedback.username}')

    return render_template('update_feedback.html' , form=form, feedback=feedback)

#integrity error in delete
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"]) 
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
    

@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/")
#Clear any information from the session and redirect to /


