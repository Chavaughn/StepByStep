from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, DateField
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
    submit = SubmitField('Add Student')