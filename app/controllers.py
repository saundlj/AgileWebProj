
# isolate logic of method returning messages
# rendering in routes file

# having method to unit test in isolation without having to respond to requests, have the server running or flash method

from datetime import date, datetime, timezone
import re
from app.models import Application, User, Post, Account
from app import db

def capitalize_first_word(title):
    words = title.split()
    if len(words) > 0:
        words[0] = words[0].capitalize()
    return ' '.join(words)

def sanitize_input(input_string, name=False, email=False, username=False, text=False, description=False):
        
        # Remove leading and trailing whitespaces
        sanitized_string = input_string.strip()
        
        if email:
            # Remove any potentially harmful characters for email addresses
            sanitized_string = re.sub(r'[^\w\s@.-]', '', sanitized_string)
            invalid_characters_found = sanitized_string != input_string
            sanitized_string = sanitized_string.lower() # case sensitive so store as lowercase
            return sanitized_string, invalid_characters_found


        if name:
            # Remove any potentially harmful characters for names
            sanitized_string = re.sub(r'[^a-zA-Z\s-]', '', sanitized_string)
            invalid_characters_found = sanitized_string != input_string
            sanitized_name = ' '.join(word.capitalize() for word in sanitized_string.split()) # capitilise first letter of name 
            return sanitized_name, invalid_characters_found
        
        if username:
            # Remove any potentially harmful characters for usernames
            sanitized_string = re.sub(r'[^\w\s.-]', '', sanitized_string)
            invalid_characters_found = sanitized_string != input_string
            sanitized_string = sanitized_string.lower() # case sensitive so store as lowercase
            return sanitized_string, invalid_characters_found


        if text:
            # Remove any potentially harmful characters for a text body 
            sanitized_string = re.sub(r"[^\w\s.&,-/':]", '', sanitized_string)
            invalid_characters_found = sanitized_string != input_string
            sanitized_title = capitalize_first_word(sanitized_string)
            return sanitized_title, invalid_characters_found

        
        if description:
            # Remove any potentially harmful characters for a description
            sanitized_string = re.sub(r'[^a-zA-Z0-9\s,;:.!?&\'"/()\-]', '', sanitized_string)
            invalid_characters_found = sanitized_string != input_string
            sanitized_title = capitalize_first_word(sanitized_string)
            return sanitized_title, invalid_characters_found


class NewUserError(Exception):
    pass

def new_user(new_user:User):

    # username errors
    new_user.username, invalid_string = sanitize_input(new_user.username, username=True)
    if invalid_string:
        raise NewUserError("Username contains at least one invalid character. Please remove and try again.")
    
    if User.query.filter_by(username=new_user.username).first(): #search database for existing user (returns none if no username exists)
        raise NewUserError("Username already exists. Please try another.")

    # first name errors
    new_user.first_name, invalid_string = sanitize_input(new_user.first_name, name=True)
    if invalid_string:
        raise NewUserError("First Name contains at least one invalid character. Please remove and try again.")
    
    # last name errors
    new_user.last_name, invalid_string = sanitize_input(new_user.last_name, name=True)
    if invalid_string:
        raise NewUserError("Last Name contains at least one invalid character. Please remove and try again.")
    
    # email errors
    new_user.email, invalid_string = sanitize_input(new_user.email, email=True)
    if invalid_string:
        raise NewUserError("Email contains at least one invalid character. Please remove and try again.")
    
    if User.query.filter_by(email=new_user.email).first(): #search database for existing email (returns none if no email exists)
        raise NewUserError("Email already registered. Please Login instead.")
    
    return new_user


class LoginUserError(Exception):
    pass

def log_in(email,password):

    #email errors
    email, invalid_string = sanitize_input(email, email=True)
    if invalid_string:
        raise LoginUserError("Email contains at least one invalid character. Please remove and try again.")
    
    user = User.query.filter_by(email=email).first() # returns none if user does not exist
    
    if not user:
        raise LoginUserError("Email entered is not registered. Try creating an account!")
    
    # password errors
    if not user.check_password(password): # check registerd password matches input
        raise LoginUserError("Password entered does not match registered email. Please try again.")

    return user

class JobPostError(Exception):
    pass

def new_job_post(post:Post):

    # Title errors
    post.title, invalid_string = sanitize_input(post.title, text=True)
    if invalid_string:
        raise JobPostError("Title contains at least one invalid character. Please remove and try again.")
    
    # check if user already has a post with the same title 
    existing_job = Post.query.filter_by(user_id=post.user_id, title=post.title).first()
    if existing_job:
        raise JobPostError("You already have a Post with the same title.")
    
    # Description errors
    post.description, invalid_string = sanitize_input(post.description, description=True)
    if invalid_string:
        raise JobPostError("Description contains at least one invalid character. Please remove and try again.")

    # Location errors
    post.location, invalid_string = sanitize_input(post.location, name=True)
    if invalid_string:
        raise JobPostError("Location contains at least one invalid character. Please remove and try again.")
    
    # Salary errors
    # volunteering then $0
    
    return post

class UserAccountFormError(Exception):
    pass

def new_bio(bio:Account):

    # Date cannot be before today
    earliest_start_datetime = datetime.combine(bio.earliest_start_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    if earliest_start_datetime < datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0):
        raise UserAccountFormError("Earliest start date cannot be before todays date!")

    # Bio errors
    bio.personal_bio, invalid_string = sanitize_input(bio.personal_bio, description=True)
    if invalid_string:
        raise UserAccountFormError("Personal Bio contains at least one invalid character. Please remove and try again.")
    
    return bio

class ApplicationFormError(Exception):
    pass

def new_application(application:Application, post:Post):

    # Cover Letter check 
    application.cover_letter, invalid_string = sanitize_input(application.cover_letter, description=True)
    if invalid_string:
        raise ApplicationFormError("Cover Letter contains at least one invalid character. Please remove and try again.")
    
    # cannot apply for own job post
    if post.user_id == application.user_id:
        raise ApplicationFormError("Cannot apply for your own job post!")
    
    return application





