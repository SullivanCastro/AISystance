from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Role
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(id=id).first()
        print(user.roles[0].__dict__)

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            return redirect("login.html")  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect("lookup.html")
    else:
        return render_template("login.html")


@auth.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')
        role = request.form.get('role')

        user = User.query.filter_by(id=id).first()  # if this returns a user, then the email already exists in database

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            return redirect("signup.html")

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(id=id, password=generate_password_hash(password, method='sha256'))
        role = Role.query.filter_by(name=role).first()
        new_user.roles.append(role)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect("login.html")
    else:
        return render_template("signup.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("login.html")
