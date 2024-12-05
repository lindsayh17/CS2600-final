"""
Catamount Community Bank
Flask Routes

Warning: This app contains deliberate security vulnerabilities
Do not use in a production environment! It is provided for security
training purposes only!

"""



from config import display
from flask import Flask, render_template, request, url_for, flash, redirect, session
from password_generator import generate_password
from users_db import get_id, add_user, check_locked, lock, get_options, get_password
from new_user import check_exist, password_strength
from password_hash import hash_pw, authenticate

app = Flask(__name__, static_folder='instance/static')

app.config.from_object('config')

# secret token created with: import secrets; print(secrets.token_hex())
app.secret_key = '9f42ca5014874c7b910ad2706e074e573d1f59dff77f72c385cef1fd67bf7257'


@app.route("/", methods=['GET', 'POST'])
def home():
    """ School portal home page """
    return render_template('home.html',
                           title="Home",
                           heading="Home",
                           show=display)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login the user. """
    # initialize attempts to 0
    if "attempts" not in session:
        session['attempts'] = 0

    if request.method == 'POST':
        # get username and password
        username = request.form.get('username')
        password = request.form.get('password')

        # get password hash from database
        pw_hash = get_password(username)

        lock_status = check_locked(get_id(username))
        # check to see if account is already locked
        if lock_status == True:
            return render_template('locked.html',
                                   title="Secure Login",
                                   heading="Secure Login")
        elif lock_status != False:
            flash(lock_status, 'alert-danger')
            return render_template('error.html',
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
                    lock_success = lock(username)
                    if lock_success == True:
                        flash("Your account has been locked.", 'alert-danger')
                        session['attempts'] = 0
                        return redirect(url_for('locked'))
                    elif lock_success != False:
                        flash(lock_success, 'alert-danger')
                        return redirect(url_for('error'))
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
            add_success = add_user(username, hashed_password, 's')
            if add_success == True:
                return redirect(url_for('options',
                                             id_=get_id(username)))
            else:
                return redirect(url_for('error'))
    return render_template('register.html',
        title="Secure Registration",
        heading="Secure Registration",
        generated_password=generate_password())

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

@app.route("/error", methods=['GET', 'POST'])
def error():
    return render_template('error.html',
                           title="Error",
                           heading="Error")