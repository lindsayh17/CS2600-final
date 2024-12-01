"""
Example SQLite Python Database
==============================

Experiment with the functions below to understand how the
database is created, data is inserted, and data is retrieved

"""
import sqlite3
from datetime import datetime


def create_db():
    """ Create table 'users' in 'users' database """
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users
                    (
                    user_id INTEGER PRIMARY KEY,
                    username text,
                    date_joined text,
                    password text,
                    access_level character,
                    attempts int
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

def get_options(user_id):
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        user_info = c.execute('SELECT access_level FROM users WHERE user_id == ?', (user_id, )).fetchone()

        if user_info[0] == 's':
            return ['Time Off', 'Pay', 'Rosters']
        elif user_info[0] == 't':
            return ['Time Off', 'Pay', 'Rosters', 'Grades']
        elif user_info[0] == 'a':
            return ['Time Report', 'Pay', 'Rosters', 'Grades', 'Time Off', 'Evals']
    except sqlite3.DatabaseError:
        return "Error. Could not retrieve user information."
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def check_locked(username):
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        user_info = c.execute('SELECT locked FROM users WHERE username == ?', (username, )).fetchone()
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

def lock(username):
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        c.executemany('UPDATE users SET locked = TRUE WHERE username == ?', (username, ))
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
    """ Example data insert into plants table """
    date_joined = str(get_date())
    data_to_insert = [(str(username), date_joined, str(password), access_level)]
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        if get_id(username):
            return False
        c.executemany("INSERT INTO users (username, date_joined, password, access_level) "
                      "VALUES (?, ?, ?, ?)", data_to_insert)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def search_db(username, password):
    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        user_info = c.execute('SELECT * FROM users WHERE username == ?', (username, )).fetchone()
        if user_info:
            if user_info[3] == password:
                return True
        else:
            return False
    except sqlite3.DatabaseError:
        return "Error. Could not retrieve user information."
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def query_db():
    """ Display all records in the plants table """
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
add_user('Teacher', 'badPassword', 't')  # Add a user to the database (calling multiple times will add additional plants)
query_db()  # View all data stored in the