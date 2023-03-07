"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import UserProfile
from app.forms import LoginForm, SignupForm
from werkzeug.security import check_password_hash

###
# Routing for your application.
###
@app.route('/')
def landing():
    """Render website's home page."""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """Render website's home page."""
    return render_template('dashboard.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Step by Step")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        # if user is already logged in, just redirect them to our secure page
        # or some other page like a dashboard
        flash('User is already logged in.', 'info')
        return redirect(url_for('home'))

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
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True
            login_user(user, remember=remember_me)

            flash('Logged in successfully.', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('upload'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        flash('User is already logged in.', 'info')
        return redirect(url_for('home'))
    
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        # Create a new user profile
        user = UserProfile(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except:
            flash('Error creating account.', 'danger')
            db.session.rollback()

    flash_errors(form)
    return render_template('signup.html', form=form)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
