from functools import wraps
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import Admin, Room, Employee, Parent, Student, Teacher, UserProfile
from app.forms import AddStudentForm, LoginForm, SignupForm
from werkzeug.security import check_password_hash



# === Flash functionality ===
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')
# ...


@app.route('/init_db')
def init_database():
    try:
        with app.app_context():
            from app import initialize_data
        flash('Database initialized successfully!', 'success')
    except Exception as e:
        flash(f'Error initializing database: {e}', 'danger')
    return redirect(url_for('landing'))

@app.route('/drop_db')
def drop_database():
    try:
        with app.app_context():
            db.reflect()
            db.drop_all()
            import subprocess
            subprocess.call(['flask', 'db', 'upgrade'])

        flash('Database dropped successfully and tables re-created!', 'success')
    except Exception as e:
        flash(f'Error dropping database: {e}', 'danger')
    return redirect(url_for('landing'))


def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

def load_child(user_profile_id):
    return db.session.query(Student, Room.class_name).\
        select_from(Student).\
        join(Parent).\
        join(Room, Student.class_id == Room.id).\
        filter(Parent.user_profile_id == user_profile_id).\
        filter(Student.id == Parent.student_id).\
        first()
def load_child_no_class(user_profile_id):
    return db.session.query(Student, Room.class_name).\
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
    return db.session.query(Employee, Room.class_name).\
        select_from(Employee).\
        join(Teacher, Teacher.employee_id == Employee.id).\
        join(Room, Teacher.class_id == Room.id).\
        filter(Employee.user_profile_id == user_profile_id).\
        first()

