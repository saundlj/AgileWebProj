from app import flaskApp
from flask import render_template,redirect, url_for, flash, request
from app.forms import CreateAccountForm, LoginForm, JobForm, ApplyForm, FeedApplyForm, FilterForm
from app import db
from app.models import *
from flask_login import current_user, login_user, logout_user, login_required
import time

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
@login_required
def JobPost():
    form = JobForm()
    if form.validate_on_submit(): #validated form
        job = Post(title=form.jobtitle.data, description=form.jobdescription.data, location = form.joblocation.data, job_type = form.jobtype.data, salary = form.salary.data, user_id = current_user.id)
        db.session.add(job)
        db.session.commit() #add to db
        flash(f'Job Posting Successfully Created for {form.jobtitle.data}!', 'success')    
    return render_template("JobPost.html", form = form) # render template so no data lost

@flaskApp.route("/feed", methods = ['GET', 'POST'])
@login_required # allows only a logged in user to access feed page
def feed():
    filter_form =  FilterForm()
    if filter_form.validate_on_submit():
        location = filter_form.location.data
        job_type = filter_form.job_type.data
        min_salary = filter_form.min_rate.data
        max_salary = filter_form.max_rate.data

        query = Post.query
        if location:
            query = query.filter(Post.location.ilike(f'%{location}%'))
        if job_type:
            query = query.filter(Post.job_type.in_(job_type))
        if min_salary is not None:
            query = query.filter(Post.salary >= min_salary)
        if max_salary is not None:
            query = query.filter(Post.salary <= max_salary)

        job_posts = query.all()

    else:
        job_posts = Post.query.all()

    for post in job_posts:
        username = User.query.get(post.user_id).username
        post.username = username 
        post.date_string = post.date_posted.strftime("%b %d %Y")

    form = FeedApplyForm()
    if form.validate_on_submit(): #validated form
        application = Application(user_id = current_user.id, cover_letter = form.cover_letter.data, post_id = form.post_id.data)
        db.session.add(application) #add to db
        db.session.commit()
        flash('Successfully Applied', 'success')
        
    current_applied = [] #check applications user has made so far
    for applicant in Application.query.all():
        if applicant.user_id == current_user.id:
            current_applied.append(applicant.post_id)

    return render_template("FeedPage.html", title = 'Feed',  posts = job_posts, form = form, current_applied = current_applied, filter_form=filter_form)


@flaskApp.route("/about")
def about():
    return render_template("AboutPage.html")


@flaskApp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('about'))

@flaskApp.route("/account", methods = ['GET', 'POST'])
@login_required # allows only a logged in user to access account page
def account():
    profile_pic = url_for('static', filename = 'user_photos/'+ current_user.image_file) # capability for user to edit profile photo 
    form = ApplyForm()

    if form.validate_on_submit(): #if from validates
        info = Account(title_apl=form.title_apl.data, health=form.health.data, earliest_start_date=form.earliest_start_date.data, personal_bio=form.personal_bio.data, user_id = current_user.id)
        db.session.add(info)
        db.session.commit() #add to db
        flash('Person biography created successfully', 'success')  

    num_jobs_applied = Application.query.filter_by(user_id=current_user.id).count()
    num_jobs_posted = Post.query.filter_by(user_id=current_user.id).count()

    #get account info of current user, order descending on id to select most recent addtion to db
    user_info = Account.query.filter(Account.user_id == current_user.id).order_by(Account.id.desc()).first()

    return render_template("AccountPage.html", title = 'Account', profile_pic = profile_pic, form = form, user_info = user_info, num_jobs_applied = num_jobs_applied, num_jobs_posted = num_jobs_posted)



@flaskApp.route("/MyJobPosts", methods = ['GET', 'POST'])
@login_required # allows only a logged in user to access account page
def myposts():
    applicant_info = []
    user_posts = Post.query.filter(Post.user_id == current_user.id) #gets current users posts
    all_post_ids = [post.id for post in user_posts] #returns all the post ids by the current user
    user_applications = Application.query.filter(Application.post_id.in_(all_post_ids)).all()

    #joins with Post on FK then filters by user's post ids
    for applicant in user_applications:
        account_info = Account.query.filter(Account.user_id == applicant.user_id).order_by(Account.id.desc()).first() 
        #get account info from account db, get most recent version of their account info
        user_info = User.query.filter(User.id == applicant.user_id).with_entities(User.email, User.first_name, User.last_name).first()
        #get user information, ONLY email, first name and last_name to not compromise users data to other users!
        applicant_info.append([applicant, account_info, user_info]) 
        #append account info as well as applicants because it contains the cover letter. Gets most up to date account info
    return render_template("MyJobPosts.html", user_posts = user_posts, applicant_info = applicant_info)

