from project import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import *
from sqlalchemy.orm import *


class Student(db.Model, UserMixin):

    __tablename__ = 'Student'

    rollno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    branch = db.Column(db.String(64))
    official_email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, rollno, name, branch, official_email, password_hash):
        self.rollno = rollno
        self.name = name
        self.branch = branch
        self.official_email = official_email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


"""
class Result(db.Model):
    
    rollno = db.Column(db.Integer,ForeignKey('Student.rollno'), primary_key=True)
    name = db.Column(db.String(64),ForeignKey('Student.name'))
    subject_code = db.Column(db.String(64))
    branch = db.Column(db.String(64),ForeignKey('Student.branch'))
    marks = db.Column(db.String(64))
    Student = db.relationship('Student')

    def __init__(self, rollno, name, subject_code, branch, marks):
        self.rollno = rollno
        self.name = name
        self.subject_code = subject_code
        self.branch = branch
        self.marks = marks

class SupplementaryExam(db.Model):
    rollno = db.Column(db.Integer,ForeignKey('Student.rollno'), primary_key=True)
    name = db.Column(db.String(64),ForeignKey('Student.name'))
    subject_code = db.Column(db.String(64),ForeignKey('result.subject_code'))
    branch = db.Column(db.String(64),ForeignKey('Student.branch'))
    # paid_status = db.Column(db.Boolean,ForeignKey('fees.paid_status'),default = False)
    student = db.relationship('Student')
    result = db.relationship('Result')
    # fees = db.relationship('Fees')

    def __init__(self, rollno, name, subject, branch, marks):
        self.rollno = rollno
        self.name = name
        self.subject = subject
        self.branch = branch
"""