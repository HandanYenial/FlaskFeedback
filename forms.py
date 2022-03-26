
from wtforms import Form, StringField, PasswordField,EmailField
from wtforms.validators import InputRequired,Length,NumberRange
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    username   = StringField("Username", validators=[InputRequired(), Length(min=1,max=20)])
    password   = PasswordField("Password", validators=[InputRequired() , Length(min=6 , max=15)])
    email      = EmailField("Email" , validators=[InputRequired(), Length(max=50)])
    first_name = StringField("First Name" , validators=[InputRequired() , Length(max=30)])
    last_name  = StringField("Last Name" , validators=[InputRequired() , Length(max=30)])


class LoginForm(FlaskForm):
    username   = StringField("Username", validators=[InputRequired(), Length(min=1,max=20)])
    password   = PasswordField("Password", validators=[InputRequired() , Length(min=6 , max=15)])

class FeedbackForm(FlaskForm):
    """Add feedback form."""

    title = StringField("Title",validators=[InputRequired(), Length(max=100)])
    content = StringField("Content",validators=[InputRequired()])


class DeleteForm(FlaskForm):
  
