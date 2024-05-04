from app import flaskApp
from flask import render_template,redirect, url_for, flash
from app.forms import CreateAccountForm, LoginForm
from app import db
from app.models import *
from flask_login import current_user, login_user, logout_user, login_required

posts = [
    {
    "title": "Software Engineer",
    "date_posted": "April 23, 2024",
    "company": "Apple",
    "location": "San Francisco, CA",
    "job_type": "Full-time",
    "salary": "$90,000 - $120,000 per year",
    "description": "Tech Innovations Inc. is seeking a talented and motivated Software Engineer to join our dynamic team in San Francisco. The successful candidate will be responsible for developing and maintaining high-quality software solutions, participating in the full software development lifecycle, and collaborating with cross-functional teams to deliver innovative products."
    },

    {
    "title": "University Lecturer in Computer Science",
    "date_posted": "April 22, 2024",
    "company": "Tech University",
    "location": "New York, NY",
    "job_type": "Full-time, Tenure-track",
    "salary": "Commensurate with experience",
    "description": "Tech University's Department of Computer Science is seeking a dedicated and enthusiastic individual to join our faculty as a full-time, tenure-track University Lecturer. The successful candidate will contribute to the department's mission of providing high-quality education in computer science, conducting research, and engaging in service activities."
    }
]


@flaskApp.route("/", methods = ['GET','POST'])
@flaskApp.route('/login', methods = ['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (form.password.data == user.password): # successful login 
            login_user(user, remember=form.remember.data)
            flash(f'Successfully Logged In!', 'success')
            return redirect(url_for('feed'))
        else:
            flash('Login Unsuccessful. Please check email and/or password', 'danger')
    return render_template("LoginPage.html", form = form, title = 'Login')

@flaskApp.route('/CreateAccount', methods = ['GET','POST'])
def createAccount():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    
    form = CreateAccountForm()
    if form.validate_on_submit():
        # hash password?
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Successfully Created for {form.username.data}! You are now able to log in', 'success')
        return redirect(url_for('login')) # redirect to login page
    
    return render_template("CreateAccount.html", form = form, title = 'Register') # render template so no data lost

@flaskApp.route('/JobPost', methods = ['GET','POST'])
def JobPost():
    return render_template("JobPost.html") # render template so no data lost


@flaskApp.route("/about")
def about():
    return render_template("AboutPage.html")


@flaskApp.route("/feed", methods = ['GET', 'POST'])
@login_required # allows only a logged in user to access account page
def feed():
    return render_template("FeedPage.html", title = 'Feed', posts = posts)

@flaskApp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('about'))

@flaskApp.route("/account")
@login_required # allows only a logged in user to access account page
def account():
    profile_pic = url_for('static', filename = 'user_photos/'+ current_user.image_file)
    return render_template("AccountPage.html", title = 'Account', profile_pic = profile_pic)