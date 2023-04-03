import os
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import Admin, Room, Employee, Parent, Student, Subject, Teacher, UserProfile
from app.forms import AddStudentForm, LoginForm, SignupForm
from werkzeug.security import check_password_hash
from app.controllers.AppController import *
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from flask import make_response
from io import BytesIO

@app.route('/student_report/<int:student_id>')
def generate_report(student_id):
    student = Student.query.get(student_id)
    assignments = get_assignments_for_student(student_id)
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))

    content = []

    name = f"{student.first_name} {student.last_name}"
    content.append(Paragraph(name, styles['Title']))

    class_name = student.room.class_name
    content.append(Paragraph(f"Class: {class_name}", styles['Heading2']))

    average = student.get_average_grade()
    content.append(Paragraph(f"Average: {average}%", styles['Heading3']))

    place = student.get_place_in_class()
    content.append(Paragraph(f"Position in class: {place}", styles['Heading3']))

    dob = student.date_of_birth.strftime("%m/%d/%Y")
    content.append(Paragraph(f"Date of Birth: {dob}", styles['Normal']))

    email = student.email
    content.append(Paragraph(f"Email: {email}", styles['Normal']))

    parent = student.parent.user_profile.full_name
    content.append(Paragraph(f"Parent Name: {parent}", styles['Normal']))

    subjects = Subject.query.all()
    grades = []
    for subject in subjects:
        avg_grade = student.get_average_grade_for_subject(subject.id)
        grades.append([subject.subject_name, str(avg_grade) + '%'])
    table_data = [['Subject', 'Average Grade']] + grades
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    content.append(table)


    doc.build(content)

    pdf_data = buffer.getvalue()

    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={name}.pdf'

    return response