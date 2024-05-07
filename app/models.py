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

# helps manage user sessions in the backgroud - credit https://www.youtube.com/watch?v=CSHx6eCkmv0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=6
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
    # backref adds author column to Post indicating user
    # lazy lets us look at all posts by a user 
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"
    
    def set_password(self):
        self.password_hash = generate_password_hash(self.password_hash)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc)) # all in one UTC
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # lowercase becuase referencing column NOT class

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted})"
    