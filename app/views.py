"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os

from sqlalchemy import func
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import Admin, Assignment, Room, Employee, Grades, Parent, Student, Subject, Teacher, UserProfile
from app.forms import AddStudentForm, LoginForm, SignupForm
from werkzeug.security import check_password_hash
from app.controllers.AppController import *

###
# Routing for your application.
###
@app.route('/')
@logout_required
def landing():
    """Render website's home page."""
    return render_template('landing.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 3:
        parent = Parent.query.filter_by(user_profile_id = current_user.id).first()
        children = Student.query.filter_by(parent_id=parent.id).filter(Student.student_status != 2).join(Room).all()
        pdata= [{'Parent_Data': parent},{'Child_Data':children }]
        return render_template('parent_dashboard.html', pdata = pdata, count = len(children))
    elif current_user.user_type == 1 or current_user.user_type == 2: 
        teacher = UserProfile.query.filter_by(id=current_user.id, user_type=2).first()
        admin = UserProfile.query.filter_by(id=current_user.id, user_type=1).first()
        if not teacher and not admin:
            return render_template('404.html'), 404
        if not admin:
            employee = Employee.query.filter_by(user_profile_id=teacher.id).first()
        else:
            employee = Employee.query.filter_by(user_profile_id=admin.id).first()

        if not employee:
            flash('No employee found', 'danger')
            return render_template('404.html'), 404

        teacher_info = Teacher.query.filter_by(employee_id=employee.id).first()
        admin_info = Admin.query.filter_by(employee_id=employee.id).first()
        if not admin_info and not teacher_info:
            flash('No teacher or admin found', 'danger')
            return render_template('404.html'), 404
        elif admin_info:
            users = UserProfile.query.all()
            students = Student.query.filter(Student.student_status != 2).all()
            pagination= pagenate_list(users, "Users")
            return render_template('/employee/employee_dashboard.html', teacher=admin, teacher_info=admin_info, students = students, users = users, pagination = pagination)
        teacher_class = Room.query.filter_by(id=teacher_info.class_id).first()
        student_count = len(Student.query.filter_by(class_id=teacher_info.class_id).filter(Student.student_status == 2).all())
        # Get student information for the teacher's class
        students = Student.query.filter_by(class_id=teacher_info.class_id).filter(Student.student_status != 2).all()
    
        # Get subjects in the database
        subjects = Subject.query.all()

        # Calculate each student's average grade for each subject
        student_subject_grades = []
        for student in students:
            student_subject_grades.append({
                'student_info': student,
                'subject_grades': [
                    {
                        'subject_info': subject,
                        'avg_grade': db.session.query(func.avg(Grades.grade)).join(Assignment).\
                                    filter(Grades.student_id == student.id, Assignment.subject_id == subject.id).\
                                    scalar()
                    }
                    for subject in subjects
                ]
            })
        return render_template('/employee/employee_dashboard.html', teacher=teacher, teacher_info=teacher_info, teacher_class=teacher_class, student_count=student_count, students=students, subjects=subjects, student_subject_grades=student_subject_grades)
    








@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Step by Step Pre-School")


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
