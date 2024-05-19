from typing import List
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# import data base mode
from app import db, login_manager

# INSTRUCTIONS FOR CREATING DATABASE
# flask db init
# flask db migrate
# flask db upgrade
# db.create_all()

# INSTRUCTIONS TO CLEAR DATABASE
# db.drop_all()

# Migrate
# flask db migrate

# INSRUCTIONS FOR MIGRATING DATABASE WHEN A CHSNGE HAPPENS
# flask db upgrade

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') 
    password_hash = db.Column(db.String(128), nullable=False)
    # one to many relationship
    # backref adds user column to Post indicating user
    # lazy lets us look at all posts by a user 
    posts = db.relationship('Post', backref='posts', lazy=True)
    account_bio = db.relationship('Account', backref='accounts', lazy=True)
    applications = db.relationship('Application', backref='applications', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"
    
    # automatically handles salting
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# nullable is set to true for testing purposes
# In the Post form, all data is required.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) #replace nulls
    title = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=True, default=datetime.now(timezone.utc)) # all in one UTC
    location = db.Column(db.String(50), nullable=True)
    job_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    salary = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # lowercase because referencing column NOT class

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted})"

# nullable is set to true for testing purposes
# In the Account form, all data is required.
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_apl = db.Column(db.String(6), nullable=True)
    health = db.Column(db.String(30), nullable=True)
    earliest_start_date = db.Column(db.DateTime, nullable=True, default=datetime.now(timezone.utc))
    personal_bio = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # lowercase because referencing column NOT class

    def __repr__(self):
        return f"Account('{self.user_id}', '{self.personal_bio}', '{self.updated_at})"
    
# nullable is set to true for testing purposes
# In the Application form, all data is required.
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #refrences user table
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False) #references post table
    cover_letter = db.Column(db.Text, nullable=True) 
    post = db.relationship('Post', backref='applications')

    def __repr__(self):
        return f"Application('{self.user_id}', '{self.post_id}')"