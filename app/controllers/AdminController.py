import os
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import Admin, Room, Employee, Parent, Student, Subject, Teacher, UserProfile
from app.forms import AddStudentEmployeeForm, AddStudentForm, EditAdminForm, EditEmployeeForm, EditParentForm, EditStudentForm, LoginForm, SignupForm
from werkzeug.security import check_password_hash
from app.controllers.AppController import *


@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = UserProfile.query.get_or_404(id)
  
    try:
        if request.method == 'POST':
            if user.user_type == 2:
                form = EditEmployeeForm()
                employee = Employee.query.filter_by(user_profile_id=user.id).first()
                teacher = Teacher.query.filter_by(employee_id=employee.id).first()
                rooms = Room.query.all()
                form.class_id.choices = [(room.id, room.class_name) for room in rooms]  
                if form.validate_on_submit():
                    # Update teacher information
                    if(form.first_name.data):
                        teacher.employee.user_profile.first_name = form.first_name.data
                    if(form.last_name.data):
                        teacher.employee.user_profile.last_name = form.last_name.data
                    if(form.username.data):
                        teacher.employee.user_profile.username = form.username.data
                    if(form.password.data):
                        teacher.employee.user_profile.set_password(form.password.data)
                    if(form.class_id.data):
                        teacher.class_id = form.class_id.data
                    db.session.commit()
                    flash('Teacher information has been updated successfully.', 'success')
                    return redirect(url_for('landing'))
                else:
                    flash_errors(form)
                    return render_template('/employee/admin/edit/edit_teacher.html',form = form, teacher=teacher, rooms = rooms)
            elif user.user_type == 3:
                form = EditParentForm()
                parent = Parent.query.filter_by(user_profile_id=user.id).first()
                if form.validate_on_submit():
                    # Update parent information
                    if(form.first_name.data):
                        parent.user_profile.first_name = form.first_name.data
                    if(form.last_name.data):
                        parent.user_profile.last_name = form.last_name.data
                    if(form.username.data):
                        parent.user_profile.username = form.username.data
                    if(form.password.data):
                        parent.user_profile.set_password(form.password.data)
                    if(form.date_of_birth.data):
                        parent.date_of_birth = form.date_of_birth.data
                    if(form.email.data):
                        parent.email = form.email.data
                    db.session.commit()
                    flash('Parent information has been updated successfully.', 'success')
                    return redirect(url_for('landing'))
                else:
                    flash_errors(form)
                    return render_template('/employee/admin/edit/edit_parent.html',form = form, parent=parent)
            elif user.user_type == 1:
                form = EditAdminForm()
                employee = Employee.query.filter_by(user_profile_id=user.id).first()
                admin = Admin.query.filter_by(employee_id=employee.id).first() 
                if form.validate_on_submit():
                    # Update admin information
                    if(form.first_name.data):
                        admin.employee.user_profile.first_name = form.first_name.data
                    if(form.last_name.data):
                        admin.employee.user_profile.last_name = form.last_name.data
                    if(form.username.data):
                        admin.employee.user_profile.username = form.username.data
                    if(form.password.data):
                        admin.employee.user_profile.set_password(form.password.data)
                    db.session.commit()
                    flash('Admin information has been updated successfully.', 'success')
                    return redirect(url_for('landing'))
                else:
                    flash_errors(form)
                    return render_template('/employee/admin/edit/edit_admin.html',form = form, admin=admin)
    except Exception as e:
        flash(f'Error updating user: {str(e)}', 'danger')
        db.session.rollback()
    if user.user_type == 2 and user is not None:
        # teacher form
        form = EditEmployeeForm()
        employee = Employee.query.filter_by(user_profile_id=user.id).first()
        teacher = Teacher.query.filter_by(employee_id=employee.id).first()
        rooms = Room.query.all()
        if rooms is not None:
            form.class_id.choices = [(room.id, room.class_name) for room in rooms]
        return render_template('/employee/admin/edit/edit_teacher.html',form = form, teacher=teacher, rooms = rooms)
    elif user.user_type == 3 and user is not None:
        # parent form
        form = EditParentForm()
        parent = Parent.query.filter_by(user_profile_id=user.id).first()
        return render_template('/employee/admin/edit/edit_parent.html',form = form, parent=parent)
    elif user.user_type == 1 and user is not None:
        # admin form
        form = EditAdminForm()
        employee = Employee.query.filter_by(user_profile_id=user.id).first()
        admin = Admin.query.filter_by(employee_id=employee.id).first()
        return render_template('/employee/admin/edit/edit_admin.html',form = form, admin=admin)
    else:
        # undefined user type
        return render_template('404.html', message='Undefined User Type or user not found')
    
@app.route('/view_student/<int:id>')    
def view_student(id):
    student = Student.query.filter_by(id = id).first()
    subjects = Subject.query.all()
    return render_template('employee/admin/view/view_student.html', student = student, subjects =subjects)

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])    
def edit_student(id):
    student = Student.query.filter_by(id = id).first()
    form = EditStudentForm()
    rooms = Room.query.all()
    if rooms is not None:
        form.class_id.choices = [(room.id, room.class_name) for room in rooms]
    parents = Parent.query.all()
    if parents is not None:
        form.parent_id.choices = [(parent.id, parent.user_profile.full_name) for parent in parents]
    if request.method == 'POST':
         if form.validate_on_submit():
            # Update admin information
            if(form.first_name.data):
                student.first_name = form.first_name.data
            if(form.last_name.data):
                student.last_name = form.last_name.data
            if(form.email.data):
                student.email = form.email.data
            if(form.date_of_birth.data):
                student.date_of_birth = form.date_of_birth.data
            if(form.class_id.data):
                student.class_id = form.class_id.data
            if(form.parent_id.data):
                student.parent_id = form.parent_id.data
            db.session.commit()
            flash('Student information has been updated successfully.', 'success')
            return redirect('/view_student/{}'.format(id))
    return render_template('employee/admin/edit/edit_student.html', student = student, form = form)

@app.route('/addstudent', methods=['POST', 'GET'])
@login_required
def addstudent():
    form = AddStudentEmployeeForm()
    rooms = Room.query.all()
    if rooms is not None:
        form.class_id.choices = [(room.id, room.class_name) for room in rooms]
    parents = Parent.query.all()
    if parents is not None:
        form.parent_id.choices = [(parent.id, parent.user_profile.full_name) for parent in parents]
    if request.method == 'POST':
        if form.validate_on_submit():
            # process the form data and add the student to the database
            add_student(
                Student(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    date_of_birth=form.date_of_birth.data,
                    email=form.email.data,
                    parent_id = form.parent_id.data,
                    class_id = form.class_id.data,
                    date_joined = datetime.now(),
                    student_status = 1
                )
            )
            return redirect('/')

    return render_template('student/addstudent.html', form=form, user=current_user)