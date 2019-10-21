from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,IntegerField
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.validators import Email,EqualTo,DataRequired
from wtforms import ValidationError
from project.model import Student
from project import db
from flask_wtf.file import FileAllowed, FileField

class LoginForm(FlaskForm):

    rollno = IntegerField('Roll No.',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):

    rollno = IntegerField('Roll No.',validators=[DataRequired()])
    name = StringField('Name',validators=[DataRequired()])
    branch = StringField('Branch',validators=[DataRequired()])
    official_email = StringField('Official Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message = 'password must match')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_rollno(self, rollno):
        if Student.query.filter_by(rollno = rollno.data).first():
            raise ValidationError('Roll no. already registered.')

    def check_email(self,field):
        if Student.query.filter_by(official_email=field.data).first():
            raise ValidationError('Email already registered!')

class SupplementaryExamForm(FlaskForm):
    """Serves purpose of registering data for a supplementary examination by a student
    (in very elementary phase as of now)
    """
    rollno = IntegerField('Roll No.', validators=[DataRequired()], render_kw={'readonly': True})
    name = StringField('Name', validators=[DataRequired()], render_kw={'readonly': True})
    subject_code = StringField('Subject Code', validators=[DataRequired()])
    branch = StringField('Branch', validators=[DataRequired()], render_kw={'readonly': True})
    submit = SubmitField('Register!')

class UpdateUserForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')