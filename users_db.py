"""
SQLite Python Database to track user information
==============================

Creates, retrieves from, and writes to the database.
The user database contains a user ID, username, the
date the user registered, a hashed password, an access
level, and an account lock flag.

"""
import sqlite3
from datetime import datetime
from password_hash import hash_pw


def create_db():
    """ Create table 'users' in 'users' database - used once for setup """
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users
                    (
                    user_id INTEGER PRIMARY KEY,
                    username text,
                    date_joined text,
                    password_hash text,
                    access_level character,
                    locked boolean
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def get_date():
    """ Generate timestamp for data inserts """
    d = datetime.now()
    return d.strftime("%m/%d/%Y, %H:%M:%S")

def get_id(username):
    """ get user ID from database """
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        user_info = c.execute('SELECT user_id FROM users WHERE username == ?', (username, )).fetchone()
        if user_info:
            return user_info[0]
        else:
            return False
    except sqlite3.DatabaseError:
        return "Error. Could not retrieve user information."
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def get_password(username):
    """ get hashed password from database """
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        user_info = c.execute('SELECT password_hash FROM users WHERE username == ?', (username, )).fetchone()
        if user_info:
            return user_info[0]
        else:
            return ''
    except sqlite3.DatabaseError:
        return "Error. Could not retrieve user information."
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def get_options(user_id):
    """
    Gets the options that should be displayed on a user's menu based on access level
    Access level is pulled from database
    :param user_id: the id for user viewing the page
    :return: the array of options for that user based on their access level
    """
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        user_info = c.execute('SELECT access_level FROM users WHERE user_id == ?', (user_id, )).fetchone()

        if user_info[0] == 's':
            return [[0, 'Time Off'], [1, 'Pay'], [2, 'Rosters']]
        elif user_info[0] == 't':
            return [[0, 'Time Off'], [1, 'Pay'], [2, 'Rosters'], [3, 'Grades']]
        elif user_info[0] == 'a':
            return [[4, 'Time Report'], [1, 'Pay'], [2, 'Rosters'], [3, 'Grades'], [0, 'Time Off'], [5, 'Evals']]
    except sqlite3.DatabaseError:
        return "Error. Could not retrieve user information."
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def check_locked(user_id):
    """
    Checks the database to see if an account is locked
    :param user_id: the id for user trying to sign in
    :return: True if the account is locked, False otherwise
    """
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        user_info = c.execute('SELECT locked FROM users WHERE user_id == ?', (user_id, )).fetchone()
        if user_info:
            return user_info[0] == 1
        else:
            return False
    except sqlite3.DatabaseError:
        return "Error. Could not retrieve user information."
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def lock(user_id):
    """
    Changes the locked status to true in the database
    :param user_id: the id for the user trying to sign in
    :return: True if account was successfully locked, error otherwise
    """
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        c.execute('UPDATE users SET locked = TRUE WHERE user_id == ?', (user_id, ))
        conn.commit()
        return True
    except sqlite3.DatabaseError:
        return "Error. Could not retrieve user information."
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def add_user(username, password, access_level):
    """
    Adds a user to the databse with specified username, password, and access level
    :param username: username for user being added
    :param password: password hash for user being added
    :param access_level: access level for user being added
    :return: False if username already exists or an error, True if successfully added
    """
    date_joined = str(get_date())
    data_to_insert = [(str(username), date_joined, str(password), access_level, False)]
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        # check to see if the username already exists
        if get_id(username):
            return False
        c.executemany("INSERT INTO users (username, date_joined, password_hash, access_level, locked) "
                      "VALUES (?, ?, ?, ?, ?)", data_to_insert)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return "Error. Could not create new user."
    except sqlite3.OperationalError:
        return "Error. Could not create new user."
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def query_db():
    """
    Used to display the table for debugging purposes
    """
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        for row in c.execute("SELECT * FROM users"):
            print(row)
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

# create_db()  # Run create_db function first time to create the database
# add_user('Admin', hash_pw('#1Admin!'), 'a')  # Add a user to the database
# add_user('Teacher', hash_pw('#1Teacher!'), 't')
# add_user('Substitute', hash_pw('#1Substitute!'), 's')
query_db()  # View all data stored in the