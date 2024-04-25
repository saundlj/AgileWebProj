from app import flaskApp
from flask import render_template,redirect, url_for
from app.forms import CreateAccountForm, loginReturn

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

@flaskApp.route("/")
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

#@flaskApp.route("/")
#def groups():
#    return "Test Page. Flask is working... or is it. Maybe now?"


@flaskApp.route("/about")
def about():
    return render_template("AboutPage.html")

@flaskApp.route("/feed")
def feed():
    return render_template("FeedPage.html", posts = posts, title = 'Feed')