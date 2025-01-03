# auth.py handles all account activities; such as creating accounts and logging in/out

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# creates a blueprint to manage authentication related routes. 
auth = Blueprint('auth', __name__)

# login route; allows both POST and GET requests (need to enter and retrieve info)
@auth.route('/login', methods=['GET', 'POST'])
def login():

    # if it's a post request, we obtain the email and password from the form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # go through the database to check whether this email exists
        user = User.query.filter_by(email = email).first()
        
        # if it does exist, then check if the password hashes are equal
        # (we encrypt the passwords using a hash function)
        # if its true, then successful login, else flash incorrect password
        # otherwise flash 'email doesn't exist'
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category = 'success')

                # logs in the user; remember=True to keep them logged in until they log out.
                login_user(user, remember=True)
                # Redirects to home page
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash("Email doesn't exist.", category='error')
    # if it's not a post request, simply return the login page. 
    return render_template("login.html", user=current_user)

# logs out the current user, but they have to be logged in for this to work
@auth.route('/logout')
@login_required
def logout():
    # uses flask_login module and redirects to login page. 
    logout_user()
    return redirect(url_for('auth.login'))

# signs up a user, which can either be a get or post request. 
@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    # if it's a post request, obtain the entered info from the form
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # checks if the email address is in the database
        user = User.query.filter_by(email = email).first()
        # if it is, then flash 'email already exists'
        # otherwise, pass the input through a range of checks and if it fails flash error
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(first_name) < 2:
            flash("First name must be greater than 2 characters.", category='error')
        elif password1 != password2:
            flash("The passwords enter do not match.", category='error')
        elif len(password1) < 8:
            flash("Password must be greater than 8 characters.", category='error')
        # if checks passed, then create a new user using the user class in the models.py file
        # the password is hashed using the werkzeug security module, and the pbkdf2 method.
        # add the user to the database and keep them logged in; don't prompt them to login again. 
        # redirect them to the home page where they can add notes. 
        else:
            new_user = User(email = email, first_name = first_name, password = generate_password_hash(password1, method = 'pbkdf2'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account created!", category='success')
            return redirect(url_for('views.home'))

    # if its a get request, then show the sign up page. 
    return render_template("sign_up.html", user=current_user)
    