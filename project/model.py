from project import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import *
from sqlalchemy.orm import *


@login_manager.user_loader
def load_user(userId):
    return Users.query.get(int(userId))
#######################user area################################
class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    userId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    # profile_image = db.Column(db.String(64),nullable=False,default='default_profile.jpg')
    # profile_image = db.Column(db.String(64)
    # , nullable=False, default = 'default_profile.jpg')

    def __init__(self,userId, name, password):
        self.userId = userId
        self.name = name
        self.password = password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return (self.userId)

class Handler(db.Model, UserMixin):
    __tablename__ = 'Handler'
    adminId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    def __init__(self,adminId, name, password):
        self.adminId = adminId
        self.name = name
        self.password = password
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_id(self):
        return (self.adminId)

class Hotels(db.Model):
    __tablename__ = 'Hotels'
    hotelId = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(64))
    address = db.Column(db.String(64))
    totalRooms = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    # profile_image = db.Column(db.String(64),nullable=False,default='default_profile.jpg')
    # profile_image = db.Column(db.String(64)
    # , nullable=False, default = 'default_profile.jpg')

    def __init__(self,hotelId, name, address, totalRooms,rating):
        self.hotelId = hotelId
        self.name = name
        self.address = address
        self.totalRooms = totalRooms
        self.rating = rating

class Rooms(db.Model):
    __tablename__ = 'Rooms'
    hotelId = db.Column(db.String(10),ForeignKey('Hotels.hotelId'),primary_key =True)
    roomNo = db.Column(db.String(64),primary_key=True)
    capacity = db.Column(db.Integer)
    status = db.Column(db.Boolean,default=True)
    # userId = db.Column(db.Integer,ForeignKey('Users.userId'),nullable = True)
    price = db.Column(db.String(40))
    # profile_image = db.Column(db.String(64),nullable=False,default='default_profile.jpg')
    # profile_image = db.Column(db.String(64)
    # , nullable=False, default = 'default_profile.jpg')

    def __init__(self,hotelId, roomNo,capacity,price):
        self.hotelId = hotelId
        self.roomNo = roomNo
        self.capacity = capacity
        self.price = price
    
    def set_userId(self,userId):
        self.userId = userId
    
    def set_status(self,status):
        self.status = status
    
    def set_price(self,price):
        self.price = price

class Facilities(db.Model):
    __tablename__ = 'Facilities'
    hotelId = db.Column(String(10),ForeignKey('Hotels.hotelId'),primary_key = True)
    gym = db.Column(Boolean,default=False)
    FoodBeverages = db.Column(Boolean,default=False)
    Parking = db.Column(Boolean,default=False)
    Tv = db.Column(Boolean,default=False)
    wifi = db.Column(Boolean,default=False)

    def __init__(self,hotelId,gym,FoodBeverages,Parking,Tv,wifi):
        self.hotelId = hotelId
        self.gym = gym
        self.FoodBeverages = FoodBeverages
        self.Parking = Parking
        self.Tv = Tv
        self.wifi = wifi       


class Room_allotted(db.Model, UserMixin):
    __tablename__ = 'Room_allotted'
    hotelId = db.Column(db.String(10),ForeignKey('Hotels.hotelId'),primary_key = True)   
    roomNo = db.Column(db.String(64),ForeignKey('Rooms.roomNo'), primary_key = True)
    userId = db.Column(db.Integer,ForeignKey('Users.userId'))
    checkIn = db.Column(db.String(25))
    chechOut = db.Column(db.String(25))
    totalMembers = db.Column(db.Integer)
    days = db.Column(db.Integer)
    rate = db.Column(db.Float)
    amount = db.Column(db.Float)
    paymentStatus = db.Column(db.Boolean,default = False)

    def __init__(self,hotelId, roomNo, userId, checkIn, chechOut,totalMembers,days,rate,amount):
        self.hotelId = hotelId
        self.roomNo = roomNo
        self.userId = userId
        self.checkIn = checkIn
        self.chechOut = chechOut
        self.totalMembers = totalMembers
        self.days = days
        self.rate = rate
        self.amount = amount

class Drafts(db.Model, UserMixin):
    __tablename__ = 'Drafts'
    hotelId = db.Column(db.String(10),ForeignKey('Hotels.hotelId'),primary_key = True)   
    roomNo = db.Column(db.String(64),ForeignKey('Rooms.roomNo'), primary_key = True)
    userId = db.Column(db.Integer,ForeignKey('Users.userId'),primary_key = True)
    checkIn = db.Column(db.String(25))
    chechOut = db.Column(db.String(25))
    totalMembers = db.Column(db.Integer)
    days = db.Column(db.Integer)
    rate = db.Column(db.Float)
    amount = db.Column(db.Float)
    paymentStatus = db.Column(db.Boolean,default = False)

    def __init__(self,hotelId, roomNo, userId, checkIn, chechOut,totalMembers,days,rate,amount):
        self.hotelId = hotelId
        self.roomNo = roomNo
        self.userId = userId
        self.checkIn = checkIn
        self.chechOut = chechOut
        self.totalMembers = totalMembers
        self.days = days
        self.rate = rate
        self.amount = amount

    def set_paymentStatus(self,status):
        self.paymentStatus = status
    # def set_userId(self,userId):
        # self.userId = userId

############### user area ends ##############################