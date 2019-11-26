from flask import *
from project import db
from project.model import Users,Handler, Rooms, Room_allotted, Drafts,Hotels,Facilities
from project.forms import UserLoginForm, RegisterForm, RoomBookForm, checkOutForm
from flask_login import login_user, current_user, logout_user, login_required
from project.picture_handler import add_profile_pic
import stripe
import os
from project.script import name,address 
from sqlalchemy import and_
from datetime import datetime
from werkzeug.urls import url_parse
# print(hotel_info)

admin = Blueprint('admin',__name__)

stripe_keys = {
  'publishable_key': "pk_test_EzB9rTKHvSb9uZwjzbv8q6kz00tdsUMFq0",
  'secret_key': "sk_test_SHwhbYRWt8S9ff2PfHhLthwq00M7u3Yppv"
}

stripe.api_key = stripe_keys['secret_key']

@admin.route('/')
def index():
    # db.drop_all()
    # db.create_all()
    return render_template('index.html')

# users area #####################################################################

@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('admin.index'))

def facilities_function():
    x = Facilities.query.all()
    L = []
    for x in x :
        facilities = {}
        if x.gym is True:
            facilities['gym'] = True
        if x.FoodBeverages is True:
            facilities['FoodBeverages'] = True
        if x.Parking is True:
            facilities['Parking'] = True  
        if x.Tv is True:
            facilities['Tv'] = True
        if x.wifi is True:
            facilities['wifi'] = True 
        L.append(facilities)  
    return L


@admin.route('/book')
def Book(): 
    recommendations = []
    if not current_user.is_anonymous:
        recommendations = recommendation_function()
    L = facilities_function()
    # print(recommendations)
    return render_template('book.html',hotel_names = name, hotel_address = address, facilities_list = L,recommendations = recommendations)

@admin.route('/signup', methods=['GET', 'POST'])
def signup():
    # if current_user.is_authenticated:
        # return redirect(url_for('admin.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users(userId=form.userId.data, name=form.name.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('admin.index'))
    return render_template('signup.html', title='Register', form=form)


# @admin.route('/userlogin', methods=['GET', 'POST'])
# def UserLogin():
#     # if current_user.is_authenticated:
#         # return redirect(url_for('admin.index'))
#     form = UserLoginForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(userId = form.userId.data).first()
#         if user is not None and user.check_password(form.password.data):
#             flash('Logged in successfully.')
#             login_user(user)
#             return redirect(url_for('admin.index'))
#         else:
#             flash('Invalid Credentials')
#             # return render_template(url_for('admin.UserLogin'))
#             return render_template('userlogin.html',form=form)
#     return render_template('userlogin.html', form=form)


@admin.route('/userlogin', methods=['GET', 'POST'])
def UserLogin():
    # if current_user.is_authenticated:
        # return redirect(url_for('admin.index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(userId = form.userId.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Credentials')
            return render_template('userlogin.html',form=form)
        # flash('Logged in successfully.')
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.index')
        return redirect(next_page)
         # return render_template(url_for('admin.UserLogin'))
    return render_template('userlogin.html', form=form)


@admin.route('/<hotelId>/book_info', methods=['GET', 'POST'])
# @login_required
def book_info(hotelId):
    if not current_user.is_authenticated:
        return redirect(url_for('admin.UserLogin'))
    # y = 'H'+hotelId
    # print(y)
    draftRooms = Drafts.query.filter_by(hotelId = hotelId,userId = current_user.userId)
    # print(draftRooms)
    draftList = []
    for each in draftRooms:
        draftList.append(each.roomNo)
    print(draftList)
    rooms = Rooms.query.filter_by(hotelId = hotelId)
    list = []
    for x in rooms:
        list.append({
            'hotelId':x.hotelId,
            'roomNo':x.roomNo,
            'capacity':x.capacity,
            'price':x.price,
            'status':x.status}
        )
    print(len(list))
    return render_template('book_info.html',list = list,draftList = draftList)

data = {}

@admin.route('/<hotelId>/<roomNo>/book_room', methods=['GET', 'POST'])
def book_room(hotelId,roomNo):
    if not current_user.is_authenticated:
        return redirect(url_for('admin.UserLogin'))
    form = RoomBookForm()
    if form.validate_on_submit():

        date_format = "%d/%m/%Y"
        print(type(form.checkIn.data))
        a = datetime.strptime( str(form.checkIn.data), date_format)
        b = datetime.strptime( str(form.checkOut.data), date_format)
        delta = b - a
        total_days =  delta.days

        rate_string = Rooms.query.filter_by(hotelId = hotelId, roomNo = roomNo).first().price
        rate = ''.join(filter(lambda i: i.isdigit(), rate_string)) 
        rate = int(rate)

        amount = rate * total_days
        print(amount,type(amount))
        data['hotelId'] = hotelId
        data['roomNo'] =  roomNo
        data['checkIn'] = form.checkIn.data
        data['checkOut'] = form.checkOut.data
        data['totalMembers'] = form.totalMembers.data
        data['amount'] = amount
        data['days'] = total_days
        data['rate'] = rate
        data['amount'] = amount
    
        return render_template('payment.html',data = data,key = stripe_keys['publishable_key'])
    return render_template('book_room.html', title = 'Book_room', form=form)   


# user area ends  ################################################################

####### for payment ###############

# @admin.route('/<dict>/paymentpage')
# def paymentpage(dict):
#     return render_template('payment.html', dict = dict, key=stripe_keys['publishable_key'])


@admin.route('/<amount>/payment', methods=['GET', 'POST'])
def payment(amount):
    # calculating total days

    # date_format = "%d/%m/%Y"
    # a = datetime.strptime( str(dict['checkIn']), date_format)
    # b = datetime.strptime( str(dict['checkOut']), date_format)
    # delta = b - a
    # total_days =  delta.days
    # print(days)

    # # calculating price rate of room

    # rate_string = Rooms.query.filter_by(hotelId = dict['hotelId'], roomNo = dict['roomNo']).first().price
    # rate = ''.join(filter(lambda i: i.isdigit(), rate_string)) 
    # rate = int(rate)
    # print(rate)

    # total_amount = rate * total_days   # total amount to be paid
    # print(amount)

    # print(dict['hotelId'])
    
    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])
    
    # CHARGE/PAYMENT INFORMATION
    # amount =Room_allotted.query.filter_by(roomNo = roomNo, hotelId = hotelId).first().amount    
    charge = stripe.Charge.create(
        customer=customer.id,
        amount = amount,
        currency='inr',
        description='Fee'
    )    

    # allot_room = Room_allotted(
    #                         roomNo = dict['roomNo'], 
    #                         hotelId = dict['hotelId'],
    #                         userId = current_user.userId,
    #                         checkIn = dict['checkIn'] , 
    #                         chechOut = dict['checkOut'], 
    #                         totalMembers = dict['totalMembers'])

    # db.session.add(allot_room)
    # db.session.commit()
    # Rooms.query.filter_by(roomNo = dict['roomNo'], hotelId = dict['hotelId']).first().status = False
    # db.session.commit()
    # x = dict['hotelId']
    # print(hotelId)
    return redirect(url_for('admin.saveData'))

@admin.route('/saveData', methods=['GET', 'POST'])
def saveData():
    hotelId = data['hotelId']
    roomNo = data['roomNo']

    allot_room = Room_allotted(
                            roomNo = data['roomNo'], 
                            hotelId = data['hotelId'],
                            userId = current_user.userId,
                            checkIn = data['checkIn'] , 
                            chechOut = data['checkOut'], 
                            totalMembers = data['totalMembers'],
                            days = data['days'],
                            rate = data['rate'],
                            amount = data['amount'])

    db.session.add(allot_room)
    db.session.commit()

    x = Rooms.query.filter_by(roomNo = roomNo, hotelId = hotelId).first()
    if x is not None:
        x.status = False
        db.session.commit()

    y = Room_allotted.query.filter_by(roomNo = roomNo, hotelId = hotelId).first()
    if y is not None:
        y.paymentStatus = True
        db.session.commit()

    z = Drafts.query.filter_by(roomNo = roomNo, hotelId = hotelId, userId = current_user.userId).first()
    if z is not None:
        z.paymentStatus = True
        db.session.commit()
    else:
        draft = Drafts(
                        hotelId = data['hotelId'],
                        userId = current_user.userId,
                        checkIn = data['checkIn'] , 
                        chechOut = data['checkOut'], 
                        totalMembers = data['totalMembers'],
                        roomNo = data['roomNo'], 
                        days = data['days'],
                        rate = data['rate'],
                        amount = data['amount'],
                        )
        draft.set_paymentStatus(True)
    
        db.session.add(draft)
        db.session.commit()
    return redirect(url_for('admin.index'))


@admin.route('/userDashboard', methods=['GET', 'POST'])
def userDashboard():
    # Rooms.query.filter_by(roomNo = roomNo, hotelId = hotelId).first().status = False
    # Room_allotted.query.filter_by(roomNo = roomNo, hotelId = hotelId).first().paymentStatus = False    
    # db.session.commit()
    x = Users.query.filter_by(userId = current_user.userId).first()
    if x is not None:
        print(x.name)
    y = drafts = Drafts.query.filter_by(userId = current_user.userId).first()
    if y is not None:
        print(y.hotelId)
    # for each in drafts:
    #     for x in each:
    #         print(x.userId,x.hotelId,x.roomNo)

    return render_template('userDashboard.html')

@admin.route('/draft', methods=['GET', 'POST'])
def draft():
    # uId = Drafts.query.filter_by(hotelId = data['hotelId'],roomNo = data['roomNo']).first()
    # if(uId is not None):
    #     if(current_user.userId == uId.userId):
    x = Drafts.query.filter_by(hotelId = data['hotelId'],roomNo = data['roomNo'], userId = current_user.userId).first()
    if (x is not None):
        x.checkIn = data['checkIn']
        x.chechOut = data['checkOut']
        x.totalMembers = data['totalMembers']
        db.session.commit()
        # flash('Draft already saved for your application')
    else:
        draft = Drafts(
                        hotelId = data['hotelId'],
                        userId = current_user.userId,
                        checkIn = data['checkIn'] , 
                        chechOut = data['checkOut'], 
                        totalMembers = data['totalMembers'],
                        roomNo = data['roomNo'], 
                        days = data['days'],
                        rate = data['rate'],
                        amount = data['amount'])
    
        db.session.add(draft)
        db.session.commit()
    
    return redirect(url_for('admin.index'))


@admin.route('/viewDraft', methods=['GET', 'POST'])
def viewDraft():
    # bookedByUser = False
    # booked = Drafts.query.filter_by(paymentStatus = True)
    # if(booked is not None):
        # bookedByUser = [x.userId == current_user.userId   for x in booked]
    drafts = Drafts.query.filter_by(userId = current_user.userId, paymentStatus = False)
    draftList = []
    if( drafts is not None):
        for each in drafts:
            draftList.append(
                {
                    'hotelId': each.hotelId,
                    'hotelName': Hotels.query.filter_by(hotelId = each.hotelId).first().name,
                    'availability': Rooms.query.filter_by(hotelId = each.hotelId, roomNo = each.roomNo).first().status,
                    'roomNo': each.roomNo,
                    'checkIn': each.checkIn,
                    'checkOut': each.chechOut,
                    'totalMembers':each.totalMembers,
                    'days': each.days,
                    'rate': each.rate,
                    'amount': each.amount,
                }
            )
    return render_template('viewDraft.html',draftList = draftList)

@admin.route('/previousBooking', methods=['GET', 'POST'])
def previousBooking():
    drafts = Drafts.query.filter_by(userId = current_user.userId, paymentStatus = True)
    # print(drafts)
    draftList = []
    if( drafts is not None):
        for each in drafts:
            draftList.append(
                {
                    'hotelId': each.hotelId,
                    'hotelName': Hotels.query.filter_by(hotelId = each.hotelId).first().name,
                    'availability': Rooms.query.filter_by(hotelId = each.hotelId, roomNo = each.roomNo).first().status,
                    'roomNo': each.roomNo,
                    'checkIn': each.checkIn,
                    'checkOut': each.chechOut,
                    'totalMembers':each.totalMembers,
                    'days': each.days,
                    'rate': each.rate,
                    'amount': each.amount,
                }
            )
    # print(len(draftList))
    return render_template('previousBooking.html',draftList = draftList)

################################ Admin Section ####################

@admin.route('/adminlogin', methods=['GET', 'POST'])
def adminLogin():
    # if current_user.is_authenticated:
        # return redirect(url_for('admin.index'))
    form = UserLoginForm()
    print('ok')
    if form.validate_on_submit():
        administrator = Handler.query.filter_by(adminId = form.userId.data).first()
        if administrator is not None and  administrator.check_password(form.password.data):
            login_user(administrator)
            return render_template('adminDashboard.html',form=form)
            
        flash('Invalid Credentials')
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
            # next_page = url_for('admin.index')
        # return redirect(next_page)
        # return render_template(url_for('admin.UserLogin'))
    return render_template('adminLogin.html',form=form)

@admin.route('/adminDashboard', methods=['GET', 'POST'])
def adminDashboard():
    return render_template('adminDashboard.html')

@admin.route('/allBookings',methods = ['GET','POST'])
def allBookings():
    bookings = Room_allotted.query.all()
    checkOutDetails = []
    list = []
    if bookings is not None:
        for each in bookings:
            list.append(
                {
                    'hotelId': each.hotelId,
                    'hotelName': Hotels.query.filter_by(hotelId = each.hotelId).first().name,
                    'roomNo':  each.roomNo,
                    'userId': each.userId,
                    'checkIn' : each.checkIn,
                    'checkOut' : each.chechOut,
                    'totalMembers' : each.totalMembers,
                    'days' : each.days,
                    'rate' : each.rate,
                    'amount' : each.amount,
                    'checkOutDetails':[
                             each.hotelId,
                             each.roomNo,
                             each.userId,
                    ]
                })

    print(list)
    print(len(list))
    return render_template('allBooking.html',list = list)


@admin.route('/checkOut', methods=['GET', 'POST'])
def checkOut():
    form = checkOutForm()
    if form.validate_on_submit():
        userId = form.userId.data
        hotelId = form.hotelId.data
        roomNo = form.roomNo.data
        # updating avalability of room
        Rooms.query.filter_by(hotelId = hotelId, roomNo = roomNo).first().status = True
        # deleting room alloted to user
        db.session.query(Room_allotted).filter_by(userId = userId,roomNo = roomNo, hotelId = hotelId).delete()
        db.session.commit()
        return redirect(url_for('admin.adminDashboard'))
    return render_template('checkOut.html', title ='', form = form)   


@admin.route('/<checkOutDetails>/checkOutDirect', methods=['GET', 'POST'])
def checkOutDirect(checkOutDetails):
    print(checkOutDetails)
    hotelId = checkOutDetails[0]
    roomNo = checkOutDetails[1]
    userId = checkOutDetails[2]
    # updating avalability of room
    x = Rooms.query.filter_by(hotelId = hotelId, roomNo = roomNo).first()
    if x is not None:
        x.status = True
    # deleting room alloted to user
    db.session.query(Room_allotted).filter_by(userId = userId,roomNo = roomNo, hotelId = hotelId).delete()
    db.session.commit()
    return redirect(url_for('admin.allBookings'))



################# Recommendation Funciton Implemented Here ################
from recommendation import similarity_hotel
def recommendation_function():
    alloted = Room_allotted.query.filter_by(userId = current_user.userId)
    booked_hotel = []
    if alloted is not None:
        for each in alloted:
            if each.hotelId not in booked_hotel:
                booked_hotel.append(each.hotelId)
    # print(booked_hotel)


    print(similarity_hotel[1][1])
    # print(similarity_hotel.shape)
    new_recommendation = []
    for each in booked_hotel:
        hotelNo = ''.join(filter(lambda i: i.isdigit(),each))
        # print(hotelNo)
        hotelNo = int(hotelNo)

        for i in range(similarity_hotel.shape[1]): # finding the hotels similar to the ones booked by user using hotel similarity matrix
            x = similarity_hotel[hotelNo][i]
            if x >= 0.94 :
                new_recommendation.append(i)
    # print(new_recommendation)
    return new_recommendation
####################  Recommendatin function ends ###############

@admin.route('/recommended')
def recommended():
    L = facilities_function()
    recommendations = recommendation_function()
    # print(recommendations)
    return render_template('recommended.html',hotel_names = name, hotel_address = address, facilities_list = L,recommendations = recommendations)
