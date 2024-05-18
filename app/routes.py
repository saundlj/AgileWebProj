from app.blueprints import main
from flask import render_template,redirect, url_for, flash, request
from app.forms import CreateAccountForm, LoginForm, JobForm, ApplyForm
from app.models import *
from flask_login import current_user, login_user, logout_user, login_required
import time
from app.controllers import NewUserError, LoginUserError, JobPostError, log_in, new_user, new_job_post

# attatch routes to blueprints and not to flaskApp
# blueprints can be created ahead of time (no configuration needed) 
@main.route("/", methods = ['GET','POST'])
@main.route("/home", methods = ['GET'])
def home():
    return render_template("home.html", title = "Home")

@main.route('/login', methods = ['GET','POST'])
def login():

    if current_user.is_authenticated: #if user is remembered 
        return redirect(url_for('main.feed'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = log_in(form.email.data,form.password.data)

        except LoginUserError as e:
            flash(e, 'danger')
            return render_template("LoginPage.html", form = form, title = 'Login')

        login_user(user, remember=form.remember.data)
        flash(f'Welcome back {user.first_name}!', 'success')
        return redirect(url_for('main.feed'))
    return render_template("LoginPage.html", form = form, title = 'Login')

@main.route('/createAccount', methods = ['GET','POST'])
def createAccount():
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))
    
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password_hash=form.password.data)
        
        # error checking and santising of form data
        try:
            user = new_user(user)
        
        except NewUserError as e:
            flash(e, 'danger')
            return render_template("CreateAccount.html", form = form, title = 'Register') # render template so no data lost
        
        user.set_password() # hash password
        db.session.add(user)
        db.session.commit()
        flash(f'Account Successfully Created for {user.username}! You are now able to log in', 'success')
        return redirect(url_for('main.login')) # redirect to login page
    
    return render_template("CreateAccount.html", form = form, title = 'Register') # render template so no data lost

@main.route('/JobPost', methods = ['GET','POST'])
def JobPost():
    form = JobForm()
    if form.validate_on_submit():
        job = Post(title=form.jobtitle.data, description=form.jobdescription.data, location = form.joblocation.data, job_type = form.jobtype.data, salary = form.salary.data, user_id = current_user.id)
        try:
            job = new_job_post(job)

        except JobPostError as e:
            flash(e, 'danger')
            return render_template("JobPost.html", form = form)

        db.session.add(job)
        db.session.commit()
        flash(f'Job Posting Successfully Created for {form.jobtitle.data}!', 'success')    
        # return to job posting page
        
    return render_template("JobPost.html", form = form) # render template so no data lost

@main.route("/posts")
def posts():
    return render_template("posts.html")

@main.route("/feed", methods = ['GET', 'POST'])
@login_required # allows only a logged in user to access account page
def feed():
    job_posts = Post.query.all()
    return render_template("FeedPage.html", title = 'Feed',  posts = job_posts )


@main.route("/about")
def about():
    return render_template("AboutPage.html")


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.about'))

@main.route("/account", methods = ['GET', 'POST'])
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



