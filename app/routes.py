from app import flaskApp
from flask import render_template,redirect, url_for, flash, request
from app.forms import CreateAccountForm, LoginForm, JobForm, ApplyForm
from app import db
from app.models import *
from flask_login import current_user, login_user, logout_user, login_required

@flaskApp.route("/", methods = ['GET','POST'])
@flaskApp.route("/home", methods = ['GET'])
def home():
    return render_template("home.html", title = "Home")

@flaskApp.route('/login', methods = ['GET','POST'])
def login():

    if current_user.is_authenticated: #if user is remembered 
        return redirect(url_for('feed'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # check email exists 
        if not user:
            flash(f"Email entered is not registered. Try creating an account!", 'danger')
            return render_template("LoginPage.html", form = form, title = 'Login')

        password = form.password.data
        if not user.check_password(password): # check password for account matches input
            flash(f'Invalid password. Please try again.', 'danger')
            return render_template("LoginPage.html", form = form, title = 'Login')
        
        login_user(user, remember=form.remember.data)
        flash(f'Successfully Logged In!', 'success')
        return redirect(url_for('feed'))
    
    return render_template("LoginPage.html", form = form, title = 'Login')

@flaskApp.route('/createAccount', methods = ['GET','POST'])
def createAccount():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password_hash=form.password.data)
        user.set_password() # hash password
        db.session.add(user)
        db.session.commit()
        flash(f'Account Successfully Created for {form.username.data}! You are now able to log in', 'success')
        return redirect(url_for('login')) # redirect to login page
    
    return render_template("CreateAccount.html", form = form, title = 'Register') # render template so no data lost

@flaskApp.route('/JobPost', methods = ['GET','POST'])
def JobPost():
    form = JobForm()
    if form.validate_on_submit():
        job = Post(title=form.jobtitle.data, description=form.jobdescription.data, location = form.joblocation.data, job_type = form.jobtype.data, salary = form.salary.data)
        db.session.add(job)
        db.session.commit()
        flash(f'Job Posting Successfully Created for {form.jobtitle.data}!', 'success')    
    return render_template("JobPost.html", form = form) # render template so no data lost


@flaskApp.route("/feed", methods = ['GET', 'POST'])
@login_required # allows only a logged in user to access account page
def feed():
    job_posts = Post.query.all()
    return render_template("FeedPage.html", title = 'Feed',  posts = job_posts )


@flaskApp.route("/about")
def about():
    return render_template("AboutPage.html")


@flaskApp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('about'))

@flaskApp.route("/account", methods = ['GET', 'POST'])
@login_required # allows only a logged in user to access account page
def account():
    profile_pic = url_for('static', filename = 'user_photos/'+ current_user.image_file)
    form = ApplyForm()
    if form.validate_on_submit():
        info = Account(title_apl=form.title_apl.data, health=form.health.data, earliest_start_date=form.earliest_start_date.data, personal_bio=form.personal_bio.data, user_id = current_user.id)
        db.session.add(info)
        db.session.commit()
        flash('Person biography created successfully')  
    user_info = Account.query.filter(Account.user_id == current_user.id).order_by(Account.id.desc()).first()
    return render_template("AccountPage.html", title = 'Account', profile_pic = profile_pic, form = form, user_info = user_info)



