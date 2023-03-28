from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import UserProfile
from app.forms import LoginForm
from werkzeug.security import check_password_hash
from app.controllers.AppController import *


# === Login functionality ===
@app.route('/parent-login', methods=['POST', 'GET'])
@logout_required
def login():
    if current_user.is_authenticated:
        # if user is already logged in, just redirect them to our secure page
        # or some other page like a dashboard
        flash('User is already logged in.', 'info')
        return redirect(url_for('dashboard'))

    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    # Login and validate the user.
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query our database to see if the username and password entered
        # match a user that is in the database.
        user = db.session.execute(db.select(UserProfile).filter_by(username=username)).scalar()

        if user is not None and check_password_hash(user.password, password):
            if user.user_type != 3:
                flash('Login not for here.', 'danger')
                logout_user()
                return render_template('login.html', form=form)

            login_user(user, remember=False)

            flash('Logged in successfully.', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)

@app.route('/employee-login', methods=['POST', 'GET'])
@logout_required
def employeelogin():
    if current_user.is_authenticated:
        # if user is already logged in, just redirect them to our secure page
        # or some other page like a dashboard
        flash('User is already logged in.', 'info')
        return redirect(url_for('dashboard'))

    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    # Login and validate the user.
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query our database to see if the username and password entered
        # match a user that is in the database.
        user = db.session.execute(db.select(UserProfile).filter_by(username=username)).scalar()

        if user is not None and check_password_hash(user.password, password):
            if user.user_type == 3:
                flash('Login not for here.', 'danger')
                logout_user()
                return render_template('login.html', form=form)
            login_user(user, remember=False)

            flash('Logged in successfully.', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('/employee/login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('landing'))

# ...