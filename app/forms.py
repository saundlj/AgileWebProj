from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, ValidationError, TextAreaField, IntegerField, SelectField, DateField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, Optional, NumberRange
from app.models import *
from sqlalchemy import func

#write flask forms in python classes below.
#e.g.
# class LoginForm(FlaskForm):
    #username = StringField('Username', validators=[DataRequired()])
    #password = PasswordField('Password', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')
    #submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=50)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')]) # repeat password
    submit = SubmitField("Create Account")

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first() #search database for existing user (returns none if no username exists)
        if user:
            raise ValidationError('Username is taken. Please choose another!')
        
    def validate_email(self, email):

        user = User.query.filter_by(email = func.lower(email.data)).first() #search database for existing user (returns none if no email exists)
        if user:
            raise ValidationError('Email is already registered. Please Login.')
        
    # Add password validator (make sure enough characters and symbols ect..)
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")


class JobForm(FlaskForm):
    jobtitle = StringField('Job Title', validators=[DataRequired()])
    jobdescription = TextAreaField('Job Description', validators=[DataRequired()])
    joblocation = StringField('Job Location', validators=[DataRequired()])
    #provide choice of job types
    jobtype_choices = [('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Casual', 'Casual'), ('Contract', 'Contract'), ('Volunteer', 'Volunteer')]
    jobtype = SelectField('Job Type', choices=jobtype_choices, validators=[DataRequired()])
    salary = IntegerField('Hourly Rate ($AUD)', validators=[NumberRange(min=0)])
    submit = SubmitField("Create")


class ApplyForm(FlaskForm):
    #provide choice of titles to user
    title_choices = [('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Miss.', 'Miss.'), ('Master.', 'Master.'), ('Madam.', 'Madam.'), ('Mx.', 'Mx.'), ('I Would Rather Not Say', 'I Would Rather Not Say')]
    title_apl = SelectField('Preferred Title', choices=title_choices, validators=[DataRequired()])
    #provide choice of health selections
    health_choices = [('Physically Able','Physically Able'), ('Not Physically Able','Not Physically Able'), ('I Would Rather Not Say', 'I Would Rather Not Say')]
    health = SelectField('Health Status', choices=health_choices, validators=[DataRequired()])
    #default start time to now
    earliest_start_date = DateField('Earliest Start Date', default=datetime.now(timezone.utc))
    personal_bio = TextAreaField('Personal Bio', validators=[DataRequired()])
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