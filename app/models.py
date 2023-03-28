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

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    admin_role = db.Column(db.Integer)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    
class Parent(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(120))
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'))

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

    def get_average_grade_for_subject(self, subject_id):
        grades = Grades.query.filter_by(student_id=self.id).join(Assignment).filter_by(subject_id=subject_id)
        avg_grade = grades.with_entities(db.func.avg(Grades.grade)).scalar()
        return round(avg_grade, 2) if avg_grade else 0.00

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


