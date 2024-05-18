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

user1 = User(username = 'testing', first_name = "test", last_name = "test", email = "admin@proj.com", password_hash = 'admin')
user2 = User(username = 'lukes', first_name = "Luke", last_name = "Saunders", email = "realemail@gmail.com", password_hash = 'admin')
user3 = User(username = 'tomv', first_name = "Tom", last_name = "Veitch", email = "tomveitch@gmail.com", password_hash = 'password')
user4 = User(username = 'vitop', first_name = "Vito", last_name = "Panaia", email = "vitopanaia@gmail.com", password_hash = 'password')
user5 = User(username = 'mattb', first_name = "Matt", last_name = "Booth", email = "mattbooth@gmail.com", password_hash = 'password')

user1.set_password(user1.password_hash) # hash password
user2.set_password(user2.password_hash) # hash password
user3.set_password(user3.password_hash) # hash password
user4.set_password(user4.password_hash) # hash password
user5.set_password(user5.password_hash) # hash password

post1 = Post(title = 'Gardener',
             date_posted = datetime(2024, 5, 13, 7, 47, 48, 223252),
             location = 'Crawley',
             job_type = 'Casual',
             description = 'Please help me do my gardening',
             salary = 40,
             user_id = 1
             )

post2 = Post(title = 'Carer',
             date_posted = datetime(2024, 5, 12, 7, 47, 48, 223252),
             location = 'Mount Lawley',
             job_type = 'Contract',
             description = 'My elderly mother (80yo) is is need of a carer for the next 2 weeks. No prior experience required. Ideal job for someone studying nursing.',
             salary = 40,
             user_id = 2
             )

post3 = Post(title='Childcare Assistant',
            date_posted=datetime(2024, 5, 14, 9, 0, 0),
            location='Fremantle',
            job_type='Casual',
            description='Looking for a responsible individual to assist with childcare at a local daycare center. Must enjoy working with children and have a friendly demeanor.',
            salary=25,
            user_id=2
            )

post4 = Post(title='Community Clean-Up Volunteer',
            date_posted=datetime(2024, 5, 15, 14, 15, 0),
            location='Perth CBD',
            job_type='Volunteer',
            description='Join us in our efforts to clean up litter and beautify public spaces in the city. Help make a positive impact on the environment and community!',
            salary=0,
            user_id=4
            )

post5 = Post(title='Food Bank Assistant',
            date_posted=datetime(2024, 5, 16, 11, 45, 0),
            location='Midland',
            job_type='Volunteer',
            description='Assist with sorting and distributing food donations at a local food bank. Help provide essential support to individuals and families in need.',
            salary=20,
            user_id=4
            )

post6 = Post(title='Tutoring Opportunity',
            date_posted=datetime(2024, 5, 17, 13, 0, 0),
            location='Joondalup',
            job_type='Part-Time',
            description='Seeking a tutor to help high school students with math and science subjects. Must have strong knowledge in the respective subjects and excellent communication skills.',
            salary=50,
            user_id=3
            )

post7 = Post(title='Community Event Coordinator',
            date_posted=datetime(2024, 5, 18, 16, 30, 0),
            location='Rockingham',
            job_type='Contract',
            description='Coordinate and plan community events and activities for a local neighborhood association. Must be creative, organized, and have experience in event planning.',
            salary=45,
            user_id=3
            )

post8 = Post(title='Animal Shelter Volunteer',
            date_posted=datetime(2024, 5, 19, 10, 0, 0),
            location='Armadale',
            job_type='Volunteer',
            description='Join our team at the local animal shelter and assist with caring for animals, cleaning enclosures, and interacting with visitors. Animal lovers welcome!',
            salary=0,
            user_id=3
            )

post9 = Post(title='Youth Mentor',
            date_posted=datetime(2024, 5, 20, 12, 0, 0),
            location='Canning Vale',
            job_type='Part-Time',
            description='Become a mentor for at-risk youth in the community. Provide guidance, support, and positive role modeling to help young people reach their full potential.',
            salary=35,
            user_id=2
            )

post10 = Post(title='Community Garden Coordinator',
            date_posted=datetime(2024, 5, 21, 9, 30, 0),
            location='Victoria Park',
            job_type='Part-Time',
            description='Manage and coordinate activities at a local community garden, including planting, maintenance, and organizing workshops. Passion for gardening and community engagement required.',
            salary=25,
            user_id=2
            )

post11 = Post(title='Homeless Shelter Volunteer',
            date_posted=datetime(2024, 5, 22, 14, 0, 0),
            location='Mandurah',
            job_type='Volunteer',
            description='Volunteer at a homeless shelter and assist with meal preparation, distribution, and providing a supportive environment for shelter residents. Make a difference in the lives of those in need.',
            salary=0,
            user_id=2
            )

post12 = Post(title='Environmental Cleanup Crew Member',
            date_posted=datetime(2024, 5, 23, 11, 0, 0),
            location='Bunbury',
            job_type='Part-Time',
            description='Join a team dedicated to preserving the environment by participating in clean-up efforts along beaches, parks, and waterways. Help protect natural habitats and wildlife.',
            salary=20,
            user_id=2
            )


db.session.add_all([user1, user2, user3, user4, user5, post1, post2, post3, post4, post5, post6, post7, post8, post9, post10, post11, post12])
db.session.commit()

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