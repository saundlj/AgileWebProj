from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#write flask forms in python classes below.
#e.g.
# class LoginForm(FlaskForm):
    #username = StringField('Username', validators=[DataRequired()])
    #password = PasswordField('Password', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')
    #submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')]) # repeat password
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")