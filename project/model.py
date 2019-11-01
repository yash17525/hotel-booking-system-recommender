from project import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import *
from sqlalchemy.orm import *


@login_manager.user_loader
def load_user(rollno):
    return Student.query.get(rollno)

class Student(db.Model, UserMixin):
    __tablename__ = 'Student'
    rollno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    branch = db.Column(db.String(64))
    official_email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.jpg')
    # profile_image = db.Column(db.String(64), nullable=False, default = 'default_profile.jpg')

    def __init__(self, rollno, name, branch, official_email, password):
        self.rollno = rollno
        self.name = name
        self.branch = branch
        self.official_email = official_email
        self.password = password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return (self.rollno)

    def __repr__(self):
        return '<Name: {}, Email: {}, Password: {}>'.format(self.name, self.official_email, self.password)

class SupplementaryExam(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rollno = db.Column(db.Integer)
    name = db.Column(db.String(64))
    subject_code = db.Column(db.String(64))
    branch = db.Column(db.String(64))
#     paid_status = db.Column(db.Boolean,ForeignKey('fees.paid_status'),default = False)
#     student = db.relationship('Student')
#     result = db.relationship('Result')
#     fees = db.relationship('Fees')

    def __init__(self, rollno, name, subject_code, branch):
        self.rollno = rollno
        self.name = name
        self.subject_code = subject_code
        self.branch = branch



#############################################################################################################################################################

# Result Database FIXED
class Result(db.Model):
    __tablename__ = 'Result'
    rollno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    branch = db.Column(db.String(64))
    sem1 = db.Column(db.String(256))
    sem2 = db.Column(db.String(256))
    sem3 = db.Column(db.String(256))
    sem4 = db.Column(db.String(256))
    sem5 = db.Column(db.String(256))
    sem6 = db.Column(db.String(256))
    sem7 = db.Column(db.String(256))
    sem8 = db.Column(db.String(256))
    sem9 = db.Column(db.String(256))
    sem10 = db.Column(db.String(256))


    # '1; DBMS:A, MaS:A, SST:B, EVS:B'
    #  DBMS:A, MaS:A, SST:B, EVS:B
    def __init__(self, rollno, name, branch, sem1, sem2, sem3, sem4, sem5, sem6, sem7, sem8, sem9, sem10):
        self.rollno = rollno
        self.name = name
        self.branch = branch
        self.sem1 = sem1
        self.sem2 = sem2
        self.sem3 = sem3
        self.sem4 = sem4
        self.sem5 = sem5
        self.sem6 = sem6
        self.sem7 = sem7
        self.sem8 = sem8
        self.sem9 = sem9
        self.sem10 = sem10

    def __repr__(self):
        return '<RollNo: {}, Name: {}, Branch: {}, sem1: {}, sem2: {}, sem3: {}>'.format(self.rollno, self.name, self.branch, self.sem1, self.sem2, self.sem3)

# Teachers Database FIXED
class Teachers(db.Model, UserMixin):
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), primary_key=True)
    dept = db.Column(db.String(64))
    password = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    def __init__(self, name, email, dept, password):
        self.name = name
        self.email = email
        self.dept = dept
        self.password = password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return (self.email)

    def __repr__(self):
        return '<Name: {}, Email: {}, Password: {}>'.format(self.name, self.email, self.password)

# Enrollments Database FIXED

class Enrollments(db.Model):
    rollno = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64), primary_key=True)
    payment = db.Column(db.String(64))
    def __init__(self, rollno, subject):
        self.rollno = rollno
        self.subject = subject
        self.payment = 0

    def __repr__(self):
        return '<RollNo: {}, Subject: {}>'.format(self.rollno, self.subject)