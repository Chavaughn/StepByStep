import os
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import Admin, Class, Employee, Parent, Student, Teacher, UserProfile
from app.forms import AddStudentForm, LoginForm, SignupForm
from werkzeug.security import check_password_hash
from app.controllers.AppController import *


@app.route("/view_student/<int:student_id>")
@login_required
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("view_student.html", student=student)