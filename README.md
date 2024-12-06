# My School Portal

Lindsay Hall
CS2660 - Cybersecurity Principles
12/6/24

---
## Setup - Database
Use the users_db file to set up the database. 
1. Uncomment the create_db function call to create the table
2. Uncomment the three add_user function calls to add users with different access levels

## Setup - Pre-made Users
Three users should be added using users_db to ensure different access levels. Otherwise, 
the users will all have the least privileged access level (substitute). The usernames and 
passwords are listed below, but can be added as described in database set up. 
* Admin: #1Admin! 
* Teacher: #1Teacher!
* Substitute: #1Substitute!

---
## Program Description
This program requires users to enter a username and password
to be given a list of options. These options are based off of
a menu a school system might have for teachers. There are three
different access levels: substitute, teacher, and administrator.
Substitutes will only have access to Time Reporting, Pay Stubs,
and Class Rosters. Teachers will have access to Pay Stubs, Class
Rosters, Student Grades, and Time Off Requests. Administrators
will be able to access Time Reporting, Pay Stubs, Class Rosters,
Student Grades, Time Off Requests, and Teacher Evaluations (all 
options).

* Substitute: Time Reporting, Pay Stubs, Class Rosters
* Teacher: Pay Stubs, Class Roster, Student Grades, Time Off Requests
* Administrator: Time Reporting, Pay Stubs, Class Rosters, 
    Student Grades, Time Off Requests, Evaluations

If a user enters the wrong password 3 times, their account will be
permanently locked. 

When registering, a user must choose a unique username and a password 
that meets the following requirements:
* 8-25 characters
* one lowercase letter
* one capital letter
* one special character
* one number

The database stores a user id, usernames, hashed passwords, date joined, 
access levels, and whether the account is locked. When a user registers, 
their password is hashed before being stored. 

---
## Testing
1. Try all pages in the flask app to ensure all display correctly (must log in to see options because user id required)
2. Try each pre-made user (after setting up database) and ensure options match access level
3. Click each link in option menus to view option page - just used as placeholder
4. Register a new user then log in
5. Ensure new user has lowest access level options
6. Try to log in with an incorrect password 3 times to lock account
7. Close page then attempt to log in as locked user again (will immediately lock again)
8. Change a SQL query in lock or check_locked, then try to register to view error page
9. Try to create an account with a username that already exists
10. Register with invalid passwords - wrong length, lacking a lowercase, uppercase, special char, or number

## Source
Sqlite: https://docs.python.org/3/library/sqlite3.html  
Sessions: https://flask.palletsprojects.com/en/stable/quickstart/#sessions  
          https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/  
Django: https://www.w3schools.com/django/django_tags_if.php  
Random Numbers: https://www.geeksforgeeks.org/random-numbers-in-python/  
                https://www.w3schools.com/python/ref_random_randint.asp  
Catamount Community Bank starter code - Professor Jim Eddy  
SQL Injection Protection from Lab 4.0  
Salting and Hashing from Lab 6.0    
Password Hash: https://www.geeksforgeeks.org/how-to-convert-bytes-to-string-in-python/  