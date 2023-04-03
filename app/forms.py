from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, DateField, SelectField
from wtforms.validators import InputRequired, EqualTo, Email
from flask_wtf.file import FileAllowed, DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class SignupForm(FlaskForm):
    username = StringField('*Username', validators=[InputRequired()])
    firstname = StringField('*First Name', validators=[DataRequired()])
    lastname = StringField('*Last Name', validators=[DataRequired()])
    email = StringField('*Email', validators=[DataRequired(), Email()])
    password = PasswordField('*Password', validators=[DataRequired()])
    confirm_password = PasswordField('*Confirm Password', validators=[DataRequired(), EqualTo('password')])
    date_of_birth = DateField('*Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class AddStudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    class_id = SelectField('Class', validators=[DataRequired()])
    submit = SubmitField('Add Student')

class AddStudentEmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    class_id = SelectField('Class', validators=[DataRequired()])
    parent_id = SelectField('Parent', validators=[DataRequired()])
    submit = SubmitField('Add Student')

class EditEmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm New Password')
    class_id = SelectField('Class Name')

class EditAdminForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm New Password')

class EditParentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm New Password')
    date_of_birth = DateField('*Date of Birth', validators=[DataRequired()])
    email = StringField('*Email', validators=[DataRequired(), Email()])

class EditStudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('*Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('*Date of Birth', validators=[DataRequired()])
    class_id = SelectField('Class')
    parent_id = SelectField('Parent')