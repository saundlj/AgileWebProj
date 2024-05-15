from app import db
from app.models import *

# dummy data

# TO RUN 
# flask shell
# import test_data

# TO ACCESS DATA
# User.query.all()
# User.query.first()
# User.query.filter_by(username = 'saundlj').first()
# user = ^^
# user.id 
# User.query.get(1)

user1 = User(username = 'testing', first_name = "test", last_name = "test", email = "admin@proj.com", password_hash = 'Admin2002')

user1.set_password() # hash password

post1 = Post(title = 'Test Post',
             location = 'Somewhere Important',
             job_type = 'Life',
             description = 'This data is stored in the database',
             user_id = 1
             )

user2 = User(username = 'saundlj', first_name = "Luke", last_name = "Saunders", email = "realemail@gmail.com", password_hash = 'Admin2002')

user2.set_password() # hash password

post2 = Post(title = 'Software Engineer',
             location = 'San Francisco, CA',
             job_type = 'Full-Time',
             description = 'Job by Apple',
             user_id = 2
             )

post3 = Post(
    title = "Software Engineer",
    location = "San Francisco, CA",
    job_type = "Full-time",
    description = "Tech Innovations Inc. is seeking a talented and motivated Software Engineer to join our dynamic team in San Francisco. The successful candidate will be responsible for developing and maintaining high-quality software solutions, participating in the full software development lifecycle, and collaborating with cross-functional teams to deliver innovative products.",
    salary = 50,
    user_id = 2
)

post4 = Post(
    title = "University Lecturer in Computer Science",
    location =  "New York, NY",
    job_type = "Full-time",
    salary = 90000,
    description = "Tech University's Department of Computer Science is seeking a dedicated and enthusiastic individual to join our faculty as a full-time, tenure-track University Lecturer. The successful candidate will contribute to the department's mission of providing high-quality education in computer science, conducting research, and engaging in service activities.",
    user_id = 2
)


post4 = Post(
    title = "University Lecturer in Computer Science",
    location = "New York, NY",
    job_type =  "Full-time",
    salary = 50000,
    description = "Tech University's Department of Computer Science is seeking a dedicated and enthusiastic individual to join our faculty as a full-time, tenure-track University Lecturer. The successful candidate will contribute to the department's mission of providing high-quality education in computer science, conducting research, and engaging in service activities.",
    user_id = 1
)

db.session.add_all([user1, post1, user2, post2, post3, post4])
db.session.commit()

def add_test_user_to_db():
    db.session.add_all([user1, post1, user2, post2, post3, post4])
    db.session.commit()

def add_test_post_to_db():
    db.session.add_all([user1, post1, user2, post2, post3, post4])
    db.session.commit()