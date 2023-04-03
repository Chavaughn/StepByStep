from datetime import datetime, timedelta
from . import db
from werkzeug.security import generate_password_hash


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    user_type = db.Column(db.Integer)
    def __init__(self, first_name, last_name, username, password, usertype):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.user_type = usertype

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.id  # python 2 support
        except NameError:
            return self.id  # python 3 support

    def get_usertype(self):
        return self.user_type

    def __repr__(self):
        return '<User %r>' % (self.username)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'))
    role = db.Column(db.Integer)
    user_profile = db.relationship('UserProfile', backref='employee')


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    admin_role = db.Column(db.Integer)
    employee = db.relationship('Employee', backref='admins')


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    employee = db.relationship('Employee', backref='teachers')
    room = db.relationship('Room', backref='teachers')
    
class Parent(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(120))
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'))
    user_profile = db.relationship('UserProfile', backref='parents')


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(120))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    student_status = db.Column(db.Integer)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    date_joined = db.Column(db.Date)
    room = db.relationship('Room', backref='students')
    parent = db.relationship('Parent', backref='students')

    @staticmethod
    def update_old_students():
        # Calculate the date 7 years ago from today
        seven_years_ago = datetime.now().date() - timedelta(days=7*365)
        Student.query.filter(Student.date_joined <= seven_years_ago).update({Student.student_status: 2})
        # Commit the changes to the database
        db.session.commit()

    def get_average_grade_for_subject(self, subject_id):
        grades = Grades.query.filter_by(student_id=self.id).join(Assignment).filter_by(subject_id=subject_id)
        avg_grade = grades.with_entities(db.func.sum(Grades.grade)).scalar()
        max_grade = Assignment.query.filter_by(subject_id=subject_id).with_entities(db.func.sum(Assignment.max_grade)).scalar()
        percentage = round((avg_grade / max_grade) * 100, 2) if max_grade and avg_grade else 0.00
        return percentage
    
    def get_average_grade(self):
        grades = Grades.query.filter_by(student_id=self.id).all()
        total_grade = sum(grade.grade for grade in grades)
        max_grade = sum(grade.assignment.max_grade for grade in grades)
        percentage = round((total_grade / max_grade) * 100, 2) if max_grade and total_grade > 0 else 0.00
        return percentage


    def get_grade_for_assignment(self, assignment_id):
        grade_obj = Grades.query.filter_by(student_id=self.id, assignment_id=assignment_id).first()
        return grade_obj.grade if grade_obj else ""
    
    def get_place_in_class(self):
        students = Student.query.filter_by(class_id=self.class_id).all()
        student_grades = {}
        for student in students:
            avg_grade = student.get_average_grade()
            student_grades[student.id] = avg_grade
        sorted_grades = {k: v for k, v in sorted(student_grades.items(), key=lambda item: item[1], reverse=True)}
        rank = 1
        for student_id, avg_grade in sorted_grades.items():
            if student_id == self.id:
                return rank
            rank += 1
        return None


class Room(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(80))

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    assignment_name = db.Column(db.String(80))
    assignment_details = db.Column(db.String(8000))
    max_grade = db.Column(db.Float)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    subject = db.relationship('Subject', backref='assignments')

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(80))
    
class Grades(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    grade = db.Column(db.Float)
    assignment = db.relationship('Assignment', backref='grades')


