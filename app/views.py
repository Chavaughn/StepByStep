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
from app.models import Admin, Assignment, Class, Employee, Grades, Parent, Student, Subject, Teacher, UserProfile
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
        result = load_child(current_user.get_id())
        if result == None:
            result = load_child_no_class(current_user.get_id())
            if result == None:
                return render_template('parent_dashboard.html', user=current_user, student=None)
        student, student_class = result
        if student is None:
            return render_template('parent_dashboard.html', user=current_user, student=None)
        return render_template('parent_dashboard.html', user=current_user, student=student, student_class=student_class)
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
            return render_template('/employee/employee_dashboard.html', teacher=admin, teacher_info=admin_info)
        teacher_class = Class.query.filter_by(id=teacher_info.class_id).first()
        student_count = len(Student.query.filter_by(class_id=teacher_info.class_id).all())
        # Get student information for the teacher's class
        students = Student.query.filter_by(class_id=teacher_info.class_id).all()

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
