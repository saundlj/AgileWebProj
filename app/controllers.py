
# isolate logic of method returning messages
# rendering in routes file

# having method to unit test in isolation without having to respond to requests, have the server running or flash method

import re
from app.models import User
from app import db


class NewUserError(Exception):
    pass

def sanitize_input(input_string, name=False):
    
    # Remove leading and trailing whitespaces
    sanitized_string = input_string.strip()
    
    # Remove any potentially harmful characters for usernames
    sanitized_string = re.sub(r'[^\w\s.-]', '', sanitized_string)
    
    # Remove any potentially harmful characters for email addresses
    sanitized_string = re.sub(r'[^\w\s@.-]', '', sanitized_string)

    if name:
        sanitized_string = re.sub(r'[^a-zA-Z\s-]', '', sanitized_string)
        invalid_characters_found = sanitized_string != input_string
        sanitized_name = ' '.join(word.capitalize() for word in sanitized_string.split())
        return sanitized_name, invalid_characters_found
    
    else:
        # Check if the sanitized string is different from the original input
        invalid_characters_found = sanitized_string != input_string
        return sanitized_string, invalid_characters_found

def new_user(new_user):

    # username errors
    new_user.username, invalid_string = sanitize_input(new_user.username)
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
    new_user.email, invalid_string = sanitize_input(new_user.email)
    if invalid_string:
        raise NewUserError("Email contains at least one invalid character. Please remove and try again.")
    
    if User.query.filter_by(email=new_user.email).first(): #search database for existing email (returns none if no email exists)
        raise NewUserError("Email already registered. Please Login instead.")
    
    return new_user





# def createAccount():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.feed'))
    
#     form = CreateAccountForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password_hash=form.password.data)
#         username = User.query.filter_by(username=user.username).first() #search database for existing user (returns none if no username exists)
#         print(user.username)
#         print(username)
#         if username:
#             flash('Username is taken. Please choose another!', 'danger')
#             return render_template("CreateAccount.html", form = form, title = 'Register')
#         user.set_password() # hash password
#         db.session.add(user)
#         db.session.commit()
#         flash(f'Account Successfully Created for {form.username.data}! You are now able to log in', 'success')
#         return redirect(url_for('main.login')) # redirect to login page
    
#     return render_template("CreateAccount.html", form = form, title = 'Register') # render template so no data lost

# in routes
# catch error once and flash errord

# try:
#     new_user(user)

# except NewUserError as e:
#     flash(e.message, 'error')
#     return render_template(...)

# return redirect(...)