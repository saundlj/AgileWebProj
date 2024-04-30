from typing import List
from datetime import datetime, timezone

# import data base mode
from app import db

# INSTRUCTIONS FOR CREATING DATABASE
# flask db init
# flask db migrate
# flask db upgrade

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #user photo
    password = db.Column(db.String(60), nullable=False)
    # one to many relationship
    # backref adds author column to Post indicating user
    # lazy lets us look at all posts by a user 
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"
    

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
    