from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, ValidationError, TextAreaField, IntegerField, SelectField, DateField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, Optional, NumberRange
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
    jobtitle = StringField('Job Title', validators=[DataRequired(), Length(min=5, max=100, message='Title must be at least 5 characters long.')])
    jobdescription = TextAreaField('Job Description', validators=[DataRequired(), Length(min=10, max=500, message='Description must be between 10 and 1000 characters.')])
    joblocation = StringField('Job Location', validators=[DataRequired(),  Length(min=2, max=50, message='Suburb name must be between 2 and 50 characters.')])
    #provide choice of job types
    jobtype_choices = [('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Casual', 'Casual'), ('Contract', 'Contract'), ('Volunteer', 'Volunteer')]
    jobtype = SelectField('Job Type', choices=jobtype_choices, validators=[DataRequired()])
    salary = IntegerField('Hourly Rate ($AUD)', validators=[NumberRange(min=0)])
    submit = SubmitField("Create")


class UserAccountForm(FlaskForm):
    #provide choice of titles to user
    title_choices = [('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Miss.', 'Miss.'), ('Master.', 'Master.'), ('Madam.', 'Madam.'), ('Mx.', 'Mx.'), ('I Would Rather Not Say', 'I Would Rather Not Say')]
    title_apl = SelectField('Preferred Title', choices=title_choices, validators=[DataRequired()])
    #provide choice of health selections
    health_choices = [('Physically Able','Physically Able'), ('Not Physically Able','Not Physically Able'), ('I Would Rather Not Say', 'I Would Rather Not Say')]
    health = SelectField('Health Status', choices=health_choices, validators=[DataRequired()])
    #default start time to now
    earliest_start_date = DateField('Earliest Start Date', default=datetime.now(timezone.utc))
    personal_bio = TextAreaField('Personal Bio', validators=[DataRequired(), Length(min=10, max=500, message='Description must be between 10 and 1000 characters.')])
    submit = SubmitField("Submit")

class FeedApplyForm(FlaskForm):
    cover_letter = TextAreaField('Cover Letter', validators=[DataRequired()])
    post_id = IntegerField('Post ID')
    submit = SubmitField("Submit")

class FeedApplyForm(FlaskForm):
    cover_letter = TextAreaField('Cover Letter', validators=[DataRequired()])
    post_id = IntegerField('Post ID')
    submit = SubmitField("Submit")

class FilterForm(FlaskForm):
    location = StringField('Location', validators=[Optional()])
    job_type = SelectMultipleField('Job Type', choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Casual', 'Casual'), ('Contract', 'Contract'), ('Volunteer', 'Volunteer')],
                                   validators=[Optional()], widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    min_rate = IntegerField('Min Rate', validators=[Optional()])
    max_rate = IntegerField('Max Rate', validators=[Optional()])
    submit = SubmitField('Apply Filter')

class DeletePostForm(FlaskForm):
    post_id = IntegerField('Post ID', validators=[DataRequired()])
    submit = SubmitField('Delete Post')

class DeleteApplication(FlaskForm):
    application_id = IntegerField('Application ID', validators=[DataRequired()])
    submit = SubmitField('Delete Application')