import os
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import Admin, Grades, Room, Employee, Parent, Student, Subject, Teacher, UserProfile
from app.forms import AddStudentForm, LoginForm, SignupForm
from werkzeug.security import check_password_hash
from app.controllers.AppController import *


@app.route("/view_student/<int:student_id>")
@login_required
def view_student_teacher(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("404.html", student=student)

@app.route("/edit_grades/<int:id>", methods=['POST', 'GET'])
@login_required
def edit_grades(id):
    student = Student.query.get_or_404(id)
    subjects = Subject.query.all()
    if request.method == "POST":
        for subject in subjects:
            for assignment in subject.assignments:
                grade = request.form.get(f"{subject.id}_{assignment.id}")
                if grade:
                    grade_obj = Grades.query.filter_by(student_id=student.id, assignment_id=assignment.id).first()
                    if not grade_obj:
                        grade_obj = Grades(student_id=student.id, assignment_id=assignment.id)
                    grade_obj.grade = float(grade)
                    db.session.add(grade_obj)
        db.session.commit()
        flash("Grades updated successfully", "success")
        return redirect(url_for("view_student", id=id))
    return render_template("employee/teacher/editstudentgrades.html", student=student, subjects=subjects)