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
from app.models import Admin, Class, Employee, Parent, Student, Teacher, UserProfile
from app.forms import AddStudentForm, LoginForm, SignupForm
from werkzeug.security import check_password_hash

###
# Routing for your application.
###
@app.route('/')
def landing():
    """Render website's home page."""
    return render_template('landing.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 2:
        result = load_child(current_user.get_id())
        if result == None:
            result = load_child_no_class(current_user.get_id())
            if result == None:
                return render_template('parent_dashboard.html', user=current_user, student=None)
        student, student_class = result
        if student is None:
            return render_template('parent_dashboard.html', user=current_user, student=None)
        return render_template('parent_dashboard.html', user=current_user, student=student, student_class=student_class)
    elif current_user.user_type == 1: 
        employee = load_employee(current_user.get_id())
        teacherclass, teacherclassname = load_teacherclass(current_user.get_id())
        if employee is None:
            return render_template('employee_dashboard.html', user=current_user, employee=None , employee_class = None)
        return render_template('employee_dashboard.html', user=current_user, employee=employee , employee_class = teacherclassname)

    return render_template('employee_dashboard.html', user=current_user)

@app.route('/student/viewstudent')
@login_required
def viewstudentparent():
    student = load_child(current_user.get_id())
    if student is None:
        return render_template('student/viewstudent.html', user=current_user, student=None)

    return render_template('student/viewstudent.html', user=current_user, student=student.student)

@app.route('/employee/assign_students_to_class', methods=['GET', 'POST'])
@login_required
def assign_students_to_class():
    if current_user.user_type == 1 or (current_user.user_type == 2 and current_user.employee.role == 2):
        # Only admins or teachers can access this page
        students = Student.query.all()
        classes = Class.query.all()
        if request.method == 'POST':
            try:
                student_id = request.form.get('student')
                class_id = int(request.form.get('class'))
                student = Student.query.get(student_id)
                student.class_id = class_id
                db.session.commit()
                flash('Student assigned to class successfully!', 'success')
                return redirect(url_for('assign_students_to_class'))
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'danger')
                db.session.rollback()
        return render_template('employee/assign_students_to_class.html', students=students, classes=classes)
    else:
        # Redirect to unauthorized page if user does not have permission
        return redirect(url_for('unauthorized'))



@app.route('/student/addstudent', methods=['POST', 'GET'])
@login_required
def addstudent():
    form = AddStudentForm()
    if form.validate_on_submit():
        # process the form data and add the student to the database
        try:
            new_student = Student(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                date_of_birth=form.date_of_birth.data,
                email=form.email.data,
            )
            db.session.add(new_student)
            db.session.commit()
            parent = Parent.query.filter_by(user_profile_id=current_user.id).first()
            if parent:
                parent.student_id = new_student.id
                db.session.add(parent)
                db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
                flash('Error creating account: '+str(e), 'danger')
                db.session.rollback()
    return render_template('student/addstudent.html', form=form, user=current_user)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Step by Step Pre-School")

@app.route('/login', methods=['POST', 'GET'])
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
            print("User Found")
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True
            login_user(user, remember=remember_me)

            flash('Logged in successfully.', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)

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


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

def load_child(user_profile_id):
    return db.session.query(Student, Class.class_name).\
        select_from(Student).\
        join(Parent).\
        join(Class, Student.class_id == Class.id).\
        filter(Parent.user_profile_id == user_profile_id).\
        filter(Student.id == Parent.student_id).\
        first()
def load_child_no_class(user_profile_id):
    return db.session.query(Student, Class.class_name).\
        select_from(Student).\
        join(Parent).\
        filter(Parent.user_profile_id == user_profile_id).\
        filter(Student.id == Parent.student_id).\
        first()

def load_employee(user_profile_id):
    return db.session.query(Employee).\
        filter(Employee.user_profile_id == user_profile_id).\
        first()

def load_teacherclass(user_profile_id):
    return db.session.query(Employee, Class.class_name).\
        select_from(Employee).\
        join(Teacher, Teacher.employee_id == Employee.id).\
        join(Class, Teacher.class_id == Class.id).\
        filter(Employee.user_profile_id == user_profile_id).\
        first()

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('landing'))


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
