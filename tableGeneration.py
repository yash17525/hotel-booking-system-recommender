from project import db
from project.model import Hotels,Rooms,Facilities
from project.script import name,address

print(len(name))
############### adding hotels to Hotels-Table ###################

for i in range(0,5):
    hotel = Hotels(hotelId='H'+str(i),name=str(name[i]),address = str(address[i]),totalRooms=10,rating=5)
    db.session.add(hotel)
    db.session.commit()

for i in range(5,11):
    hotel = Hotels(hotelId='H'+str(i),name=str(name[i]),address = str(address[i]),totalRooms=5,rating=4.6)
    db.session.add(hotel)
    db.session.commit()

for i in range(11,16):
    hotel = Hotels(hotelId='H'+str(i),name=str(name[i]),address = str(address[i]),totalRooms=5,rating=3.9)
    db.session.add(hotel)
    db.session.commit()

for i in range(16,22):
    hotel = Hotels(hotelId='H'+str(i),name=str(name[i]),address = str(address[i]),totalRooms=5,rating=4.2)
    db.session.add(hotel)
    db.session.commit()

# hotel = Hotels(hotelId='H'+str(22),name=str(name[0]),address = str(address[0]),totalRooms=5,rating=4.2)
# db.session.add(hotel)
# db.session.commit()

########## Adding rooms to the hotels ############
price = [0,10000,3000,5000,4000,6000]
x =1
for i in range(0,5):
    if x%5 == 0:
            x = 1
    for j in range(1,11):
        room = Rooms(hotelId = 'H'+str(i), roomNo = 'R' + str(j), capacity = 2, price = 'Rs.'+ str(price[x]) + ' per day' )
        db.session.add(room)
        db.session.commit()
    x = x + 1

x = 1 
for i in range(5,22):
    if x%5 == 0:
            x = 1
    for j in range(1,6):
        room = Rooms(hotelId = 'H'+str(i), roomNo = 'R' + str(j), capacity = 2, price = 'Rs.'+ str(price[x]) + ' per day' )
        db.session.add(room)
        db.session.commit()
    x = x + 1

f1 = Facilities('H1',True,True,True,True,True)
f2 = Facilities('H2',False,True,False,True,False)
f3 = Facilities('H3',True,True,True,True,True)
f4 = Facilities('H4',False,True,False,True,False)
f5 = Facilities('H5',True,True,True,True,True)
f6 = Facilities('H6',False,True,True,True,False)
f7 = Facilities('H7',True,True,True,True,True)
f8 = Facilities('H8',False,True,False,True,True)
f9 = Facilities('H9',True,True,True,True,True)
f10 = Facilities('H10',False,True,True,True,False)
f11 = Facilities('H11',True,True,True,True,True)
f12 = Facilities('H12',True,True,False,True,True)
f13 = Facilities('H13',True,True,True,True,True)
f14 = Facilities('H14',True,True,True,True,False)
f15 = Facilities('H15',True,True,True,True,True)
f16 = Facilities('H16',False,True,False,True,True)
f17 = Facilities('H17',True,True,True,True,False)
f18 = Facilities('H18',True,True,False,True,True)
f19 = Facilities('H19',False,True,True,True,True)
f20 = Facilities('H20',True,True,True,True,False)
f21 = Facilities('H21',True,True,False,True,True)
f22 = Facilities('H22',False,True,True,True,True)

db.session.add(f1)
db.session.add(f2)
db.session.add(f3)
db.session.add(f4)
db.session.add(f5)
db.session.add(f6)
db.session.add(f7)
db.session.add(f8)
db.session.add(f9)
db.session.add(f10)
db.session.add(f11)
db.session.add(f12)
db.session.add(f13)
db.session.add(f14)
db.session.add(f15)
db.session.add(f16)
db.session.add(f17)
db.session.add(f18)
db.session.add(f19)
db.session.add(f20)
db.session.add(f21)
db.session.add(f22)

db.session.commit()

