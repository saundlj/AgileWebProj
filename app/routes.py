from app import flaskApp
from flask import render_template,redirect, url_for, flash
from app.forms import CreateAccountForm, LoginForm

@flaskApp.route("/", methods = ['GET','POST'])
@flaskApp.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@proj.com' and form.password.data == 'admin':
            flash(f'Successfully Logged In!', 'success')
            return redirect(url_for('feed'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template("LoginPage.html", form = form, title = 'Login')

@flaskApp.route('/CreateAccount', methods = ['GET','POST'])
def createAccount():
    form = CreateAccountForm()
    if form.validate_on_submit():
        flash(f'Account Successfully Created for {form.first_name.data}!', 'success')
        return redirect(url_for('feed')) # redirect to home page where user can select what they want to see?
    
    return render_template("CreateAccount.html", form = form, title = 'Register') # render template so no data lost


@flaskApp.route("/about")
def about():
    return render_template("AboutPage.html")


@flaskApp.route("/feed", methods = ['GET', 'POST'])
def feed():
    return render_template("FeedPage.html", title = 'Feed')