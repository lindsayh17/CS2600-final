"""
Catamount Community Bank
Flask Routes

Warning: This app contains deliberate security vulnerabilities
Do not use in a production environment! It is provided for security
training purposes only!

"""


import csv
from tabnanny import check

from config import display
from flask import Flask, render_template, request, url_for, flash, redirect, session
from db import Db
from password_generator import generate_password
from users_db import search_db, get_id, add_user, check_locked, lock, get_options, get_password
from new_user import check_exist, password_strength
from password_hash import hash_pw, authenticate

app = Flask(__name__, static_folder='instance/static')

app.config.from_object('config')

# secret token created with: import secrets; print(secrets.token_hex())
app.secret_key = '9f42ca5014874c7b910ad2706e074e573d1f59dff77f72c385cef1fd67bf7257'


@app.route("/", methods=['GET', 'POST'])
def home():
    """ Bank home page """
    return render_template('home.html',
                           title="Home Page",
                           heading="Home Page",
                           show=display)


# @app.route("/transactions", methods=['GET', 'POST'])
# def transactions():
#     """ Transaction injection attack """
#     search_term = ''
#     if request.method == 'POST':
#         search_term = request.form.get('search_term')
#         q = sql_injection.create_search_query(1234, search_term)
#     else:
#         q = 'SELECT * FROM trnsaction WHERE trnsaction.account_id = 1234'
#     cnx = Db.get_connection()
#     c = Db.execute_query(cnx, q)
#     rows = c.fetchall()
#     return render_template('transactions.html',
#                            search_term=search_term,
#                            rows=rows,
#                            query=q,
#                            title="My Transactions",
#                            heading="My Transactions")


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login the user. """
    if "attempts" not in session:
        session['attempts'] = 0

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        pw_hash = get_password(username)

        # check to see if account is already locked
        if check_locked(username) == True:
            return render_template('locked.html',
                                   title="Secure Login",
                                   heading="Secure Login")
        try:
            # pass in 80 because 1 byte = 2 hex values
            if authenticate(pw_hash, password, 80):
                session['attempts'] = 0
                return redirect(url_for('options',
                                        id_=get_id(username)))
            else:
                session['attempts'] += 1

                # lock account after 3 attempts
                if session['attempts'] > 2:
                    lock(username)
                    flash("Your account has been locked.", 'alert-danger')
                    session['attempts'] = 0
                    return render_template('locked.html',
                                           title="Secure Login",
                                           heading="Secure Login")
                else:
                    flash("Invalid username or password!",
                          'alert-danger')
        except KeyError:
            pass
    return render_template('login.html',
                           title="Secure Login",
                           heading="Secure Login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    """register the user. """

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if check_exist(username):
            flash("Username already exists!", 'alert-info')
        elif not password_strength(password):
            flash("Password is too weak. Your password must have 8-25 characters and at least one of each of the "
                  "following: lowercase, uppercase, number, special character (!@#$%^&*)", 'alert-info')
        else:
            hashed_password = hash_pw(password)
            add_user(username, hashed_password, 's')
            return redirect(url_for('options',
                                             id_=get_id(username)))
        # flash("Invalid username or password!", 'alert-danger')
    return render_template('register.html',
                           title="Secure Registration",
                           heading="Secure Registration",
                           generated_password=generate_password())


# @app.route("/login_success/<int:id_>", methods=['GET', ])
# def login_success(id_):
#     flash("Welcome! You have logged in!", 'alert-success')
#     return render_template('customer_home.html',
#                            title="Customer Home",
#                            heading="Customer Home")

@app.route("/options/<int:id_>", methods=['GET', ])
def options(id_):
    flash("Welcome! You have logged in!", 'alert-success')

    return render_template('options.html',
                           title="Customer Home",
                           heading="Customer Home",
                           option_menu=get_options(id_))

@app.route("/option_page/<int:option_id>", methods=['GET', ])
def option_page(option_id):
    flash("Welcome! You have logged in!", 'alert-success')
    option_menu = [[4, 'Time Report'], [1, 'Pay'], [2, 'Rosters'], [3, 'Grades'], [0, 'Time Off'], [5, 'Evals']]
    option = option_menu[option_id]
    return render_template('option_page.html',
                           title=option[1],
                           heading=option[1],
                           choice=option[1])

@app.route("/locked", methods=['GET', 'POST'])
def locked():
    return render_template('locked.html',
                           title="Account Locked",
                           heading="Account Locked")
