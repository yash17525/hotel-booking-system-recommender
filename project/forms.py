from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,IntegerField
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.validators import Email,EqualTo,DataRequired
from wtforms import ValidationError
from project.model import Users
from project import db
from flask_wtf.file import FileAllowed, FileField

######################   user area #################################
class RegisterForm(FlaskForm):
    
    userId = IntegerField('User Id',validators=[DataRequired()])
    name = StringField('Name',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register!')

    def validate_userId(self, userId):
        if Users.query.filter_by(userId = userId.data).first():
            raise ValidationError('user another user Id')

class RoomBookForm(FlaskForm):
    checkIn = StringField('Check-In Date',validators=[DataRequired()],render_kw={"placeholder":"dd/mm/yyyy"})
    checkOut = StringField('Check-Out Date',validators=[DataRequired()],render_kw={"placeholder":"dd/mm/yyyy"})
    totalMembers = IntegerField('Total Visiting Member',validators = [DataRequired()],render_kw={"placeholder":"Total Visiting Members"})
    submit = SubmitField('Proceed to pay')

class checkOutForm(FlaskForm):
    userId = IntegerField('UserId',validators = [DataRequired()],render_kw={"placeholder":"Enter Unique User ID"})
    hotelId = StringField('Hotel ID',validators=[DataRequired()],render_kw={"placeholder":"Enter Hotel ID"})
    roomNo = StringField('Room Number',validators=[DataRequired()],render_kw={"placeholder":"Enter Room Number"})
    submit = SubmitField('Check-Out User')
    # def validate_userId(self, userId):
        # if Users.query.filter_by(userId = userId.data).first():
            # raise ValidationError('user another user Id')

class UserLoginForm(FlaskForm):
    userId = StringField('UserId', validators=[DataRequired()], render_kw={"placeholder":"User Id"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder":"Password"})
    submit = SubmitField('Login')



################### user area ends ###################################