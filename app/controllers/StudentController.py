import os
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import Admin, Room, Employee, Parent, Student, Subject, Teacher, UserProfile
from app.forms import AddStudentForm, LoginForm, SignupForm
from werkzeug.security import check_password_hash
from app.controllers.AppController import *

@app.route('/view_student_parent/<int:id>')    
def view_student_parent(id):
    student = Student.query.filter_by(id = id).first()
    subjects = Subject.query.all()
    return render_template('student/viewstudent.html', student = student, subjects =subjects)

@app.route('/addchild', methods=['POST', 'GET'])
@login_required
def add_student_parent():
    form = AddStudentForm()
    rooms = Room.query.all()
    parent = Parent.query.filter_by(user_profile_id = current_user.id).first()
    if rooms is not None:
        form.class_id.choices = [(room.id, room.class_name) for room in rooms]
    if request.method == 'POST':
        if form.validate_on_submit():
            # process the form data and add the student to the database
            add_student(
                Student(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    date_of_birth=form.date_of_birth.data,
                    email=form.email.data,
                    parent_id = parent.id,
                    class_id = form.class_id.data,
                    date_joined = datetime.now(),
                    student_status = 1
                )
            )
            return redirect(url_for('landing'))
    return render_template('parent/addchild.html', form=form, user=current_user)

@app.route('/employee/assign_students_to_class', methods=['GET', 'POST'])
@login_required
def assign_students_to_class():
    if current_user.user_type == 1 or (current_user.user_type == 2 and current_user.employee.role == 2):
        # Only admins or teachers can access this page
        students = Student.query.filter(Student.student_status != 2).all()
        rooms = Room.query.all()
        if request.method == 'POST':
            student_id = request.form.get('student')
            class_id = int(request.form.get('class'))
            student = Student.query.get(student_id)
            change_student_class(student, class_id)
            return redirect(url_for('landing'))
        return render_template('employee/assign_students_to_class.html', students=students, rooms=rooms)
    else:
        # Redirect to unauthorized page if user does not have permission
        return redirect(url_for('unauthorized'))