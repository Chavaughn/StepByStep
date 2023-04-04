from datetime import datetime, timedelta

from functools import wraps
import os

from sqlalchemy import create_engine
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import Admin, Assignment, Grades, Room, Employee, Parent, Student, Teacher, UserProfile
from app.forms import AddStudentForm, LoginForm, SignupForm
from werkzeug.security import check_password_hash
from sqlalchemy.orm import sessionmaker
from flask_paginate import Pagination, get_page_parameter


# === Flash functionality ===
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')
# ...


def pagenate_list(table_list, record_name):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page,per_page=5, total=len(table_list), search=False, record_name= record_name)
    return (pagination)

def change_student_class(student, class_id):
    try:
        student = Student.query.get(student.id)
        student.class_id = class_id
        db.session.commit()
        flash('Student assigned to class successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        db.session.rollback()


def admin_check():
    if current_user.user_type != 1:
        flash('Undefined User Type or Operation not supported', 'danger')
        return False
    return True

def teacher_check():
    if current_user.user_type != 2:
        flash('Undefined User Type or Operation not supported', 'danger')
        return False
    return True

def employee_check():
    if current_user.user_type != 2 and current_user.user_type != 1:
        flash('Undefined User Type or Operation not supported', 'danger')
        return False
    return True

def parent_check():
    if current_user.user_type != 3:
        flash('Undefined User Type or Operation not supported', 'danger')
        return False
    return True
    

def add_student(student):
    try:
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
            flash('Error creating account: '+str(e), 'danger')
            db.session.rollback()

@app.route('/archived_students')
def archived_students():
    archived_students = Student.query.filter(Student.student_status == 2).all()
    return render_template('archived_students.html', students=archived_students)

def get_assignments_for_student(student_id):
    grades = Grades.query.filter_by(student_id=student_id).all()

    assignments = []
    for grade in grades:
        assignment = Assignment.query.filter_by(id=grade.assignment_id).first()
        assignments.append(assignment)

    return assignments

@app.route('/init_db')
def init_database():
    try:
        with app.app_context():
            from app import initialize_data
            update_old_students()
        flash('Database initialized successfully!', 'success')
    except Exception as e:
        flash(f'Error initializing database: {e}', 'danger')
    return redirect(url_for('landing'))

@app.route('/update_old_students')
def update_old_students():
    Student.update_old_students()
    return 'Old students updated'

@app.route('/drop_db')
@login_required
def drop_database():
    try:
        logout_user()
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        Session = sessionmaker(bind=engine)
        session = Session()
        session.close_all()
        print("Logged out user")
        with app.app_context():
            db.reflect()
            print("Reflected database")
            db.drop_all()
            print("Dropped all tables")
            import subprocess
            subprocess.call(['flask', 'db', 'upgrade'])
            print("Upgraded database")
        flash('Database dropped successfully and tables re-created!', 'success')
    except Exception as e:
        flash(f'Error dropping database: {e}', 'danger')
        print(f'Error dropping database: {e}')
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

