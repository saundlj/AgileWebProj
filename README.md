# AgileWebProj
Project for Agile Web Dev: 

Compass

Application Purpose:
The purpose of this application is to connect community members through jobs. Currently, there is a significant demand for a community job posting service that prioritizes community-based connections over professionalism. An example of this style of job posting service is Facebook communities, which post local jobs for people in the area.

Our application aims to facilitate community-based connections by offering a platform tailored to the unique needs of local job seekers and job posters (or both!). The intention of our app is to allow users to sign up with a specified location and see job posts within a defined range of that location. For example, users would be able to see posts from the Greater Perth Area. Although we haven't fully implemented this feature yet, users can still navigate through the app as if they live in the Greater Perth Area.

Some key features and functionalities of our application are:

User Accounts:

- Users can create an account and log in to access the platform’s features.
- Users can manage their profiles, including updating personal information and their personal bio.

Job Postings:

- Users can view all job postings available on the platform.
- Job postings can be filtered and sorted based on various criteria to help users find relevant opportunities quickly.
- Users can apply to job postings directly through the platform.
- A user can also create new job postings and manage existing ones.
- User can see all people who have applied for their job (ideally select their ideal candidate but at the moment its up to the user to email their selected candidate)

Application Management:

- Users can view and manage their job applications, including the ability to delete applications if needed.
- Job posters can review applications submitted for their job postings.

Consistent Design and Usability:

- The application is designed using Flask
- It utilizes a SQLite3 database for development purposes, with plans to migrate to a MySQL database upon deployment for enhanced scalability and performance.
- A layout page ensures consistent styling across all pages, providing a cohesive and user-friendly interface.

Security and Data Integrity:

- The application includes extensive data validation and sanitization to prevent malicious input and ensure data integrity.
- Security measures are in place to protect user information and maintain a secure database environment.

Main Pages:

Create Account Page:

Users can create an account by entering their username, first name, last name, email, and password.
Validation ensures that the username or email is not already registered.
User passwords are hashed and salted before being stored in the database for security.

Login Page:

Users can log in using their email and password entered during account creation.
Appropriate error messages are displayed if an unregistered email is entered or if the password does not match the database records.

Feed Page:

Connects job applicants to job postings.
Users can apply to jobs by submitting their personal information and cover letter.
Users can filter job postings and apply to any job (except their own).
Users can navigate to view their own job postings or the jobs they have applied to.

Account Page:

Users can view and update their personal information.
The page summarizes the number of jobs applied to and the number of jobs posted, with links to the respective pages.

My Job Posts Page:

Users can view all job posts they have created and see details of applicants who have applied.
Users can delete jobs they have created.

My Applications Page:

Users can view all the jobs they have applied to.
Users can delete their applications if they no longer want to apply or if they want to update their information.

StudentID       Name               Git Username
23381469        Tom Veitch         tomve1tch
23073972	    Matt Booth         mjb44552
23003472	    Luke Saunders      saundlj
23443635	    Vittorio Panai     vittopan


How to launch the application:
1. Clone github repository and navigate to project directory 
2. Create and activate a virtual environment
3. Download libraries and packages. 
    Run: pip install -r requirements.txt
4. Launch App
    Run: python projectify.py

When running this code, the app will pre-populate with some existing users and posts. This is done to give you an idea of how users may collaborate in a feed page with some existing data. You are free to create an account or log in using the test credentials (email: "realemail@gmail.com", password: "admin").

How to run tests:
 Note: We were unable to get selenium tests running. Only unit testings exist for this project. 
1. Clone github repository and navigate to project directory 
2. Create and activate a virtual environment
3. Download libraries and packages. 
    Run: pip install -r requirements.txt
4. Run Tests
    Run: python -m unittest tests/unit.py

There are 14 unit tests which comprehensively cover form data before entering the database or allowing the user to procede. 