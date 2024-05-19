from app.blueprints import main
from flask import render_template,redirect, url_for, flash, request
from app.forms import CreateAccountForm, LoginForm, JobForm, UserAccountForm, FeedApplyForm, FilterForm, DeletePostForm, DeleteApplication
from app import db
from app.models import User, Post, Account, Application
from datetime import datetime, timezone
from flask_login import current_user, login_user, logout_user, login_required
import time
from app.controllers import NewUserError, LoginUserError, JobPostError, UserAccountFormError, ApplicationFormError, log_in, new_user, new_job_post, new_bio, new_application

# attatch routes to blueprints and not to flaskApp
# blueprints can be created ahead of time (no configuration needed) 
@main.route("/", methods = ['GET','POST'])
@main.route("/home", methods = ['GET'])
def home():
    return render_template("home.html", title = "Home")

# login page 
@main.route('/login', methods = ['GET','POST'])
def login():

    if current_user.is_authenticated: #if user is remembered 
        return redirect(url_for('main.feed'))
    
    form = LoginForm()

    # string validation and error checking is done in controller.py
    if form.validate_on_submit():
        try:
            user = log_in(form.email.data,form.password.data)

        # if there is an error while the user tries to log in, re render the login page so the user doesn't lose form data. Present error message. 
        except LoginUserError as e:
            flash(e, 'danger')
            return render_template("LoginPage.html", form = form, title = 'Login')

        # direct user to feed page if successfully logged in
        login_user(user, remember=form.remember.data)
        flash(f'Welcome back {user.first_name}!', 'success')
        return redirect(url_for('main.feed'))
    return render_template("LoginPage.html", form = form, title = 'Login')

@main.route('/createAccount', methods = ['GET','POST'])
def createAccount():

    # if user is already authenticated (remember me ticked or logged in), redirect to feed page
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))
    
    form = CreateAccountForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password_hash=form.password.data)
        
        # error checking and santising of form data in controllers.py
        try:
            user = new_user(user)
        
        except NewUserError as e:
            flash(e, 'danger')
            return render_template("CreateAccount.html", form = form, title = 'Register') # render template so no data lost
        
        user.set_password(user.password_hash) # hash password
        db.session.add(user)
        db.session.commit()
        flash(f'Account Successfully Created for {user.username}! You are now able to log in', 'success')
        return redirect(url_for('main.login')) # redirect to login page
    
    return render_template("CreateAccount.html", form = form, title = 'Register') # render template so no data lost

@main.route('/JobPost', methods = ['GET','POST'])
@login_required # user must be autheticated and logged in to access this page
def JobPost():
    form = JobForm()
    if form.validate_on_submit():
        job = Post(title=form.jobtitle.data, description=form.jobdescription.data, location = form.joblocation.data, job_type = form.jobtype.data, salary = form.salary.data, user_id = current_user.id)
        # data validations and sanitising of form data in controllers.py
        try:
            job = new_job_post(job)

        except JobPostError as e:
            flash(e, 'danger')
            return render_template("JobPost.html", form = form)

        db.session.add(job)
        db.session.commit() #add to db
        flash(f'Job Posting Successfully Created for {form.jobtitle.data}!', 'success')    
        # return to job posting page
        return redirect(url_for('main.myposts'))

    return render_template("JobPost.html", form = form) # render template so no data lost

@main.route("/feed", methods=['GET', 'POST'])
@login_required  # Allows only a logged in user to access feed page
def feed():
    sort_order = request.args.get('sort', 'desc')  # Get sort order from request arguments
    filter_form = FilterForm()
    if filter_form.validate_on_submit():  # If filter form is submitted and validated
        location = filter_form.location.data
        job_type = filter_form.job_type.data
        min_salary = filter_form.min_rate.data
        max_salary = filter_form.max_rate.data

        query = Post.query
        if location:
            query = query.filter(Post.location.ilike(f'%{location}%'))  # Filter posts by location
        if job_type:
            query = query.filter(Post.job_type.in_(job_type))  # Filter posts by job type
        if min_salary is not None:
            query = query.filter(Post.salary >= min_salary)  # Filter posts by minimum salary
        if max_salary is not None:
            query = query.filter(Post.salary <= max_salary)  # Filter posts by maximum salary

        if sort_order == 'asc':
            job_posts = query.order_by(Post.date_posted.asc()).all()  # Sort posts in ascending order
        else:
            job_posts = query.order_by(Post.date_posted.desc()).all()  # Sort posts in descending order
    else:
        if sort_order == 'asc':
            job_posts = Post.query.order_by(Post.date_posted.asc()).all()  # Default sort order if no filter applied
        else:
            job_posts = Post.query.order_by(Post.date_posted.desc()).all()

    # Add additional information to posts
    for post in job_posts:
        username = User.query.get(post.user_id).username
        post.username = username 
        post.date_string = post.date_posted.strftime("%b %d %Y")  # Format date to a readable string

    form = FeedApplyForm()

    if form.validate_on_submit():  # If application form is submitted and validated
        application = Application(user_id=current_user.id, cover_letter=form.cover_letter.data, post_id=form.post_id.data)
        post = Post.query.filter_by(id=form.post_id.data).first()
        try:
            application = new_application(application, post)
            db.session.add(application)  # Add to db
            db.session.commit()
            flash(f'Successfully Applied for "{post.title}"', 'success')

        except ApplicationFormError as e:
            flash(e, 'danger')
        
    current_applied = []  # Check applications user has made so far
    for applicant in Application.query.all():
        if applicant.user_id == current_user.id:
            current_applied.append(applicant.post_id)

    return render_template("FeedPage.html", title='Feed', posts=job_posts, form=form, current_applied=current_applied, filter_form=filter_form)

@main.route("/about")
def about():
    return render_template("AboutPage.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.about'))

# Current users account page with ability to update bio 
@main.route("/account", methods = ['GET', 'POST'])
@login_required # allows only a logged in user to access account page
def account():
    profile_pic = url_for('static', filename = 'user_photos/'+ current_user.image_file)
    form = UserAccountForm()
    if form.validate_on_submit():
        info = Account(title_apl=form.title_apl.data, health=form.health.data, earliest_start_date=form.earliest_start_date.data, personal_bio=form.personal_bio.data, user_id = current_user.id, updated_at=datetime.now(timezone.utc))
        try:
            info = new_bio(info)
            db.session.add(info)
            db.session.commit()
            flash('Person biography successfully updated', 'success')  

        except UserAccountFormError as e:
            flash(e, 'danger')
            # return render_template("AccountPage.html", title = 'Account', profile_pic = profile_pic, form = form, user_info = user_info)


    num_jobs_applied = Application.query.filter_by(user_id=current_user.id).count()
    num_jobs_posted = Post.query.filter_by(user_id=current_user.id).count()
        
    user_info = Account.query.filter(Account.user_id == current_user.id).order_by(Account.updated_at.desc()).first()
    return render_template("AccountPage.html", title = 'Account', profile_pic = profile_pic, form = form, user_info = user_info, num_jobs_applied = num_jobs_applied, num_jobs_posted = num_jobs_posted)

# View current users Job posts, other user data on who have applied for the job and the ability to delete them 
@main.route("/MyJobPosts", methods = ['GET', 'POST', 'DELETE'])
@login_required # allows only a logged in user to access account page
def myposts():
    applicant_info = []
    user_posts = Post.query.filter(Post.user_id == current_user.id).order_by(Post.date_posted.desc()) #gets current users posts
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

    form = DeletePostForm()
    if form.validate_on_submit():
        postid = form.post_id.data
        delete_post = Post.query.filter(Post.id == postid)
        delete_application = Application.query.filter(Application.post_id == postid)
        #finds all applications associated with post and deletes
        for old_application in delete_application:
            db.session.delete(old_application)
            db.session.commit()
        #deletes old post
        for old_post in delete_post:
            db.session.delete(old_post)
            db.session.commit()
        flash("Post Successfully Deleted!", 'danger')
    return render_template("MyJobPosts.html", user_posts = user_posts, applicant_info = applicant_info, form = form)


# View current users Job applications and the ability to delete them 
@main.route("/MyApplications", methods = ['GET', 'POST', 'DELETE'])
@login_required # allows only a logged in user to access account page
def myapplications():
    form = DeleteApplication()

    if form.validate_on_submit():
        old_application = Application.query.filter(Application.id == form.application_id.data).first()
        if old_application:
            db.session.delete(old_application)
            db.session.commit()
        flash("Application Successfully Deleted!", 'danger')

    application_data = []
    myapp = Application.query.filter(Application.user_id == current_user.id)
    for application in myapp:
        app_info = Post.query.filter(application.post_id == Post.id).first() 
        application_data.append([application, app_info])
    
    return render_template("MyApplications.html", application_data = application_data , form = form)


