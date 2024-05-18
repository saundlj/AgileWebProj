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




# db.session.add_all([user1, post1, user2, post2, post3, post4])
# db.session.commit()

def add_test_users_to_db():
    user1 = User(username = 'testing', first_name = "test", last_name = "test", email = "admin@proj.com", password_hash = 'Admin2002')

    user1.set_password(user1.password_hash) # hash password

    post1 = Post(title = 'Test Post',
                location = 'Somewhere Important',
                job_type = 'Life',
                description = 'This data is stored in the database',
                user_id = 1
                )

    user2 = User(username = 'saundlj', first_name = "Luke", last_name = "Saunders", email = "realemail@gmail.com", password_hash = 'Admin2002')

    user2.set_password(user1.password_hash) # hash password

    post2 = Post(title = 'Software Engineer',
                location = 'San Francisco, CA',
                job_type = 'Full-Time',
                description = 'Job by Apple',
                user_id = 2
                )


    db.session.add_all([user1, post1, user2, post2])
    db.session.commit()

# def add_test_post_to_db():
#     db.session.add_all([user1, post1, user2, post2, post3, post4])
#     db.session.commit()