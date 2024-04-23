from app import flaskApp
from flask import render_template,redirect, url_for
from app.forms import CreateAccountForm, loginReturn

@flaskApp.route('/login', methods = ['GET','POST'])
def login():
    form = CreateAccountForm()
    if form.validate_on_submit():
        return redirect(url_for('createAccount'))
    return render_template("LoginPage.html",form = form)

@flaskApp.route('/CreateAccount', methods = ['GET','POST'])
def createAccount():
    form = loginReturn()
    if form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template("CreateAccount.html", form = form)

@flaskApp.route("/")
def groups():
    return "Test Page. Flask is working"

