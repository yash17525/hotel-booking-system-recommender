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

    name = StringField('Name',validators=[DataRequired()])
    rollno = IntegerField('Roll No.',validators=[DataRequired()])
    branch = StringField('Branch',validators=[DataRequired()])
    official_email = StringField('Official Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message = 'password must match')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_rollno(self, field):
        if Student.query.filter_by(rollno = field.data).first():
            raise ValidationError('Sorry, roll no. already registered!')