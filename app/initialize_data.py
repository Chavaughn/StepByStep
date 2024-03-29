import datetime
import random
from app import db
from app.models import Teacher, UserProfile, Employee, Admin, Parent, Student, Room, Assignment, Subject, Grades
from datetime import date, datetime, timedelta
from nameparser import HumanName
# List of common first names
first_names = ['Olivia', 'Liam', 'Emma', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason', 'Isabella', 'Lucas', 'Mia', 'Jackson', 'Harper', 'Logan', 'Evelyn', 'Caden', 'Abigail', 'Jacob', 'Emily', 'Aiden', 'Charlotte', 'Ella', 'Elijah', 'Avery', 'Caleb', 'Sofia', 'Connor', 'Chloe', 'Makayla', 'Landon', 'Lily', 'Grayson', 'Madelyn', 'Brayden', 'Amelia', 'Bryson', 'Hannah', 'Levi', 'Natalie', 'Peyton', 'Eva', 'Cameron', 'Aria', 'Hazel', 'Caroline', 'Wyatt', 'Audrey', 'Easton', 'Aubrey', 'Brooklyn', 'Isabelle', 'Nicholas', 'Aaliyah', 'Jaxon', 'Ellie', 'Ezra', 'Addison', 'Luke', 'Alyssa', 'Oliver', 'Hailey', 'Owen', 'Anna']

# List of common last names
last_names = ['Smith', 'Johnson', 'Brown', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Perez', 'Taylor', 'Anderson', 'Wilson', 'Moore', 'Jackson', 'Martin', 'Lee', 'Lewis', 'Walker', 'Hall', 'Allen', 'Young', 'King', 'Wright', 'Scott', 'Green', 'Baker', 'Adams', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner', 'Phillips', 'Campbell', 'Parker', 'Evans', 'Edwards', 'Collins', 'Stewart', 'Sanchez', 'Morris', 'Rogers', 'Reed', 'Cook', 'Morgan', 'Bell', 'Murphy', 'Bailey', 'Rivera', 'Cooper', 'Richardson', 'Cox', 'Howard', 'Ward', 'Torres', 'Peterson', 'Gray', 'Ramirez', 'James', 'Watson', 'Brooks']



# Create user profiles
admin_user = UserProfile(first_name = random.choice(first_names), last_name=random.choice(last_names), username='admin', password='adminpass', usertype=1)
employee_user1 = UserProfile(first_name = random.choice(first_names), last_name=random.choice(last_names), username='teacher1', password='employeepass', usertype=2)
employee_user2 = UserProfile(first_name = random.choice(first_names), last_name=random.choice(last_names), username='teacher2', password='employeepass', usertype=2)
employee_user3 = UserProfile(first_name = random.choice(first_names), last_name=random.choice(last_names), username='teacher3', password='employeepass', usertype=2)
parent_user1 = UserProfile(first_name = random.choice(first_names), last_name=random.choice(last_names), username='parent1', password='parentpass', usertype=3)
parent_user2 = UserProfile(first_name = random.choice(first_names), last_name=random.choice(last_names), username='parent2', password='parentpass', usertype=3)
parent_user3 = UserProfile(first_name = random.choice(first_names), last_name=random.choice(last_names), username='parent3', password='parentpass', usertype=3)

# Add user profiles to database
db.session.add(admin_user)
db.session.add(employee_user1)
db.session.add(employee_user2)
db.session.add(employee_user3)
db.session.add(parent_user1)
db.session.add(parent_user2)
db.session.add(parent_user3)
db.session.commit()

# Create employees and link to user profiles
employee0 = Employee(user_profile_id=admin_user.id, role=0)
employee1 = Employee(user_profile_id=employee_user1.id, role=1)
employee2 = Employee(user_profile_id=employee_user2.id, role=1)
employee3 = Employee(user_profile_id=employee_user3.id, role=1)
db.session.add(employee0)
db.session.add(employee1)
db.session.add(employee2)
db.session.add(employee3)
db.session.commit()

# Create admin and link to employee
admin = Admin(employee_id=employee0.id, admin_role=1)
db.session.add(admin)
db.session.commit()

# Create some rooms
class1 = Room(class_name='Strawberry Heroes')
class2 = Room(class_name='Banana Fighters')
class3 = Room(class_name='Peach Warriors')
class4 = Room(class_name='Unassigned')
db.session.add(class1)
db.session.add(class2)
db.session.add(class3)
db.session.add(class4)
db.session.commit()

# Create teachers and link to employee and rooms
teacher1 = Teacher(employee_id=employee1.id, class_id=1)
teacher2 = Teacher(employee_id=employee2.id, class_id=2)
teacher3 = Teacher(employee_id=employee3.id, class_id=3)
db.session.add(teacher1)
db.session.add(teacher2)
db.session.add(teacher3)
db.session.commit()

# Create parents and link to user profiles and students
parent1 = Parent(date_of_birth=date(1980, 1, 1), email='parent1@example.com', user_profile_id=parent_user1.id)
parent2 = Parent(date_of_birth=date(1985, 1, 1), email='parent2@example.com', user_profile_id=parent_user2.id)
parent3 = Parent(date_of_birth=date(1982, 1, 1), email='parent3@example.com', user_profile_id=parent_user3.id)
db.session.add(parent1)
db.session.add(parent2)
db.session.add(parent3)
db.session.commit()

# Create students and link to rooms
student1 = Student(first_name='John', last_name='Doe', date_of_birth=date(2020, 1, 1), email='john.doe@example.com', class_id=class1.id, student_status=1, parent_id = parent1.id, date_joined=date(2020, 1, 1))
student2 = Student(first_name='Jane', last_name='Smith', date_of_birth=date(2019, 2, 2), email='jane.smith@example.com', class_id=class2.id, student_status=1, parent_id = parent2.id, date_joined=date(2020, 1, 1))
student3 = Student(first_name='Sarah', last_name='Johnson', date_of_birth=date(2020, 3, 3), email='sarah.johnson@example.com', class_id=class1.id, student_status=1, parent_id = parent3.id, date_joined=date(2020, 1, 1))
student4 = Student(first_name='Mark', last_name='Williams', date_of_birth=date(2021, 4, 4), email='mark.williams@example.com', class_id=class2.id, student_status=1, parent_id = parent1.id, date_joined=date(2020, 1, 1))
db.session.add(student1)
db.session.add(student2)
db.session.add(student3)
db.session.add(student4)
db.session.commit()


# Create subjects and assignments
subject1 = Subject(subject_name='Math')
subject2 = Subject(subject_name='Phonics')
subject3 = Subject(subject_name='Art')
subject4 = Subject(subject_name='Music')
db.session.add(subject1)
db.session.add(subject2)
db.session.add(subject3)
db.session.add(subject4)
db.session.commit()

assignment1 = Assignment(assignment_name='Math Assignment 1', assignment_details='Details for assignment 1', max_grade=10, class_id=class1.id, subject_id=subject1.id)
assignment2 = Assignment(assignment_name='Phonics Assignment 2', assignment_details='Details for assignment 2', max_grade=20, class_id=class2.id, subject_id=subject2.id)
assignment3 = Assignment(assignment_name='Art Assignment 3', assignment_details='Details for assignment 3', max_grade=15, class_id=class1.id, subject_id=subject3.id)
assignment4 = Assignment(assignment_name='Music Assignment 4', assignment_details='Details for assignment 4', max_grade=25, class_id=class2.id, subject_id=subject4.id)
db.session.add(assignment1)
db.session.add(assignment2)
db.session.add(assignment3)
db.session.add(assignment4)
db.session.commit()

# Create grades for students
grade1 = Grades(student_id=student1.id, assignment_id=assignment1.id, grade=8.5)
grade2 = Grades(student_id=student2.id, assignment_id=assignment2.id, grade=18.0)
grade3 = Grades(student_id=student3.id, assignment_id=assignment3.id, grade=12.0)
grade4 = Grades(student_id=student4.id, assignment_id=assignment4.id, grade=21.5)
db.session.add(grade1)
db.session.add(grade2)
db.session.add(grade3)
db.session.add(grade4)
db.session.commit()

# Get a list of all rooms in the database
rooms = Room.query.all()

# Get a list of all parents in the database
parents = Parent.query.all()
days_offset = random.randint(365*0, 365*6)
days_offset_archive = random.randint(365*6, 365*7)



# Generate and add 20 random students to the database with age 1-4 and joined within age 7
for i in range(20):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    class_id = random.choice(rooms).id
    parent_id = random.choice(parents).id
    age = random.randint(1, 4)
    date_of_birth = datetime.now() - timedelta(days=random.randint(365*age, 365*(age+1)))
    date_joined = date_of_birth + timedelta(days=random.randint(365*1, 365*3))
    email = f"student_{i+1}@example.com"
    student = Student(first_name=first_name, last_name=last_name, class_id=class_id, parent_id=parent_id, date_of_birth=date_of_birth, email=email, student_status=1, date_joined=date_joined)
    db.session.add(student)
    db.session.commit()

# Generate and add 40 random archived students to the database with age >= 7 and joined within age >= 8
for i in range(40):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    class_id = random.choice(rooms).id
    parent_id = random.choice(parents).id
    age = random.randint(7, 12)
    date_joined = datetime.now() - timedelta(days=random.randint(365*(age+1), 365*(age+2)))
    date_of_birth = date_joined - timedelta(days=random.randint(365*(age), 365*(age+1)))
    email = f"archived_{i+1}@example.com"
    student = Student(first_name=first_name, last_name=last_name, class_id=class_id, parent_id=parent_id, date_of_birth=date_of_birth, email=email, student_status=2, date_joined=date_joined)
    db.session.add(student)
    db.session.commit()



subjects = Subject.query.all()
available_rooms = [room for room in rooms if room.id != 4]
for subject in subjects:
    for i in range(5):
        assignment_name = f"{subject.subject_name}-Assignment{i+1}"
        assignment_details = f"{subject.subject_name}-Assignment{i+1} Details"
        max_grade = random.randint(10, 100)
        class_id = random.choice(available_rooms).id
        assignment = Assignment(assignment_name=assignment_name,assignment_details=assignment_details, subject_id=subject.id,class_id=class_id, max_grade=max_grade)
        db.session.add(assignment)
        db.session.commit()

students = Student.query.all()

for student in students:
    for subject in subjects:
        assignments = Assignment.query.filter_by(subject_id = subject.id)
        for assignment in assignments:
            grade = random.randint(0, assignment.max_grade)
            student_grade = Grades(student_id=student.id, assignment_id=assignment.id, grade=grade+0.00)
            db.session.add(student_grade)
            db.session.commit()
