from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, ValidationError, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired 
from app.models import *
from sqlalchemy import func
import string

#write flask forms in python classes below.
#e.g.
# class LoginForm(FlaskForm):
    #username = StringField('Username', validators=[DataRequired()])
    #password = PasswordField('Password', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')
    #submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm):

    # function to check for the presence of a capital letter
    def has_capital_letter(form, field):
        if not any(char.isupper() for char in field.data):
            raise ValidationError('Password must contain at least one capital letter\n')

    # function to check for the presence of a special character
    def has_special_character(form, field):
        special_characters = string.punctuation
        numbers = string.digits
        if not any(char in special_characters or char in numbers for char in field.data):
            raise ValidationError('Password must contain at least one special character or number\n')


    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=50)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=5, message='Password must be at least 5 characters long'),
        has_capital_letter,
        has_special_character
    ])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')]) # repeat password
    submit = SubmitField("Create Account")

    # Define a function to check for the presence of a capital letter
   
    # def validate_username(self, username):

    #     user = User.query.filter_by(username=username.data).first() #search database for existing user (returns none if no username exists)
    #     if user:
    #         raise ValidationError('Username is taken. Please choose another!')
        
    # def validate_email(self, email):

    #     user = User.query.filter_by(email = func.lower(email.data)).first() #search database for existing user (returns none if no email exists)
    #     if user:
    #         raise ValidationError('Email is already registered. Please Login.')
        
    # # Add password validator (make sure enough characters and symbols ect..)
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")


class JobForm(FlaskForm):
    jobtitle = StringField('Job Title', validators=[DataRequired()])
    jobdescription = TextAreaField('Job Description', validators=[DataRequired()])
    joblocation = StringField('Job Location', validators=[DataRequired()])
    jobtype_choices = [('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Casual', 'Casual'), ('Contract', 'Contract')]
    jobtype = SelectField('Job Type', choices=jobtype_choices, validators=[DataRequired()])
    salary = IntegerField('Job Salary ($AUD)', validators=[DataRequired()])
    submit = SubmitField("Create")


class ApplyForm(FlaskForm):
    title_choices = [('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Miss.', 'Miss.'), ('Master.', 'Master.'), ('Madam.', 'Madam.'), ('Mx.', 'Mx.')]
    title_apl = SelectField('Preferred Title', choices=title_choices, validators=[DataRequired()])
    health_choices = [('Physically Able','Physically Able'), ('Not Physically Able','Not Physically Able'), ('I Would Rather Not Say', 'I Would Rather Not Say')]
    health = SelectField('Health Status', choices=health_choices, validators=[DataRequired()])
    earliest_start_date = DateField('Earliest Start Date', default=datetime.now(timezone.utc))
    personal_bio = TextAreaField('Personal Bio', validators=[DataRequired()])
    submit = SubmitField("Submit")