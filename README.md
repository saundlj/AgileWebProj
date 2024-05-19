# AgileWebProj
Project for Agile Web Dev: 

Compass

Application Purpose:
The purpose of this application is to connect community members through jobs. Currently, there is a large demand for a community job posting service which caters to community based connections over professionalism. An example of this style of job posting service is the facebook communities which post local jobs for people in the area. Our website allows users to create an account, login, view all job postings, filter and sort job posting, apply to job postings, create job postings, view their job positings, delete their job postings, view their applications, delete their applications, create infromation about their account, submit a cover letter and their personal information to job posters. This application is designed using flask, connected to a sqlite3 database which we will hopefully change into a mysql database when deploying this application. The utilisation of a layout page allows a consistent styling to be deployed across all other pages (as specified by the layout page). 

Main Pages:

-Create Account Page
Users can create an account entering their username, first name, last name, email and password.

-Login Page
Users can login using their password and email as entered on the create account page.

-Home Page
Automatically redirect on login and when first entering the website to the homepage. Provides users with explanation about our website and our purpose.

-Feed Page
Connects job applicants to job postings. Users can apply to jobs, submitting their personal info and cover letter. Users can sort and filter jobs to meet their specifications.

-Account Page
Users can view their personal information they have entered, as well as update their information which is submitted to job posters.

-My Job Posts Page
Users can view any job posts they have made as well as the details of applicants who have applied. Users can also delete jobs which they have created. 

-My Applications Page
Users can view all the jobs they have applied to and delete their application from jobs they no longer want to apply to, or if they want to update their information. 


StudentID       Name               Git Username
23381469        Tom Veitch         tomve1tch
23073972	    Matt Booth         mjb44552
23003472	    Luke Saunders      saundlj
23443635	    Vittorio Panai     vittopan


How to launch the application:
1. Download github repository
2. From github directory, create and activate a virtual environment
3. Run: pip install -r requirements.txt
4. 

