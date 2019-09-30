from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,IntegerField
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.validators import Email,EqualTo,DataRequired
from wtforms import ValidationError
from project.model import Student
from project import db

class LoginForm(FlaskForm):

    rollno = IntegerField('Roll No.',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('LogIn')

class RegisterForm(FlaskForm):

    rollno = IntegerField('Roll No.',validators=[DataRequired()])
    name = StringField('Name',validators=[DataRequired()])
    branch = StringField('Branch',validators=[DataRequired()])
    official_email = db.Column(db.String(64), unique=True)
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message = 'password must match')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_rollno(self, field):
        if Student.query.filter_by(rollno = field.data).first():
            raise ValidationError('Sorry, roll no. already registered!')

class SupplementaryExamForm(FlaskForm):
    """Serves purpose of registering data for a supplementary examination by a student
    (in very elementary phase as of now)
    """
    rollno = IntegerField('Roll No.', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    subject_code = StringField('Subject Code', validators=[DataRequired()])
    branch = StringField('Branch', validators=[DataRequired()])
    submit = SubmitField('Register!')