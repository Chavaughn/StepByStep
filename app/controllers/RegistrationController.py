from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from app.models import Parent, UserProfile
from app.forms import SignupForm
from app.controllers.AppController import *

# === Register functionality ===

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        flash('User is already logged in.', 'info')
        return redirect(url_for('landing'))

    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        password = form.password.data
        email = form.email.data
        date_of_birth = form.date_of_birth.data

        # Create a new user profile
        user = UserProfile(username=username,first_name=firstname,last_name=lastname, password=password, usertype=2)

        # Create a new parent
        parent = Parent(date_of_birth=date_of_birth, email=email, user_profile_id=user.get_id())

        try:
            db.session.add(user)
            db.session.add(parent)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error creating account: ', 'danger')
            db.session.rollback()


    flash_errors(form)
    return render_template('signup.html', form=form)

# ...