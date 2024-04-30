from app import flaskApp
from flask import render_template,redirect, url_for, flash
from app.forms import CreateAccountForm, LoginForm
from app import db
from app.models import *

@flaskApp.route("/", methods = ['GET','POST'])
@flaskApp.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@proj.com' and form.password.data == 'admin':
            flash(f'Successfully Logged In!', 'success')
            return redirect(url_for('feed'))
        else:
            flash('Login Unsuccessful. Please check email and/or password', 'danger')
    
    return render_template("LoginPage.html", form = form, title = 'Login')

@flaskApp.route('/CreateAccount', methods = ['GET','POST'])
def createAccount():
    form = CreateAccountForm()
    if form.validate_on_submit():
        # hash password?
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Successfully Created for {form.username.data}! You are now able to log in', 'success')
        return redirect(url_for('login')) # redirect to login page
    
    return render_template("CreateAccount.html", form = form, title = 'Register') # render template so no data lost


@flaskApp.route("/about")
def about():
    return render_template("AboutPage.html")


@flaskApp.route("/feed", methods = ['GET', 'POST'])
def feed():
    return render_template("FeedPage.html", title = 'Feed')