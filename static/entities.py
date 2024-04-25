from static import db, bcrypt
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Enum
from sqlalchemy.ext.hybrid import hybrid_property

# Association Table
dropOff = db.Table(
    'dropOff',
    db.Column('dropOffID', db.Integer, primary_key=True),
    db.Column('fromLocation', db.Integer, db.ForeignKey('address.addressID'), nullable=True),
    db.Column('toLocation', db.Integer, db.ForeignKey('address.addressID'), nullable=True),
    db.Column('classID', db.Integer, db.ForeignKey('carClass.carClassID'), nullable=True),
    db.Column('charge', db.Integer, nullable=False)
)

#Strong Entities
class Address(db.Model):
    __tablename__ = 'address'
    addressID = db.Column(db.Integer, primary_key=True)
    streetName = db.Column(db.String(50), nullable=False)
    streetNumber = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    postalCode = db.Column(db.String(50), nullable=False)
    
    @hybrid_property
    def fullAddressName(self):
        return f"{self.streetNumber} {self.streetName}, {self.city}, {self.province}, {self.postalCode}"
    
    #an address can be shared by many users
    users = db.relationship('User', backref='person')
    
    #an address is a location assigned that can be shared by many employees
    employees = db.relationship('Employee', backref='location', foreign_keys='Employee.locationAssignedID')
    
    #an address can be shared by many rents including to and from location
    toRents = db.relationship('Rent', backref='toPlace', foreign_keys='Rent.locationDropOffID')
    fromRents = db.relationship('Rent', backref='fromPlace', foreign_keys='Rent.locationRentedID')
    
    #many-to-many relationship with Car Class
    fromClass = db.relationship('CarClass', secondary=dropOff, 
                                foreign_keys='[dropOff.c.fromLocation, dropOff.c.classID]',
                                backref=db.backref('fromLoc', lazy='dynamic'), overlaps="fromLoc,fromClass")
    
    toClass = db.relationship('CarClass', secondary=dropOff, 
                              foreign_keys='[dropOff.c.toLocation, dropOff.c.classID]',
                              backref=db.backref('toLoc', lazy='dynamic'), overlaps="toLoc,toClass")

class CarClass(db.Model):
    __tablename__ = 'carClass'
    carClassID = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(Enum('sedans', 'luxury', 'compacts', 'subcompacts'), nullable=False)
    
    #a car class can have many cars
    cars = db.relationship('Car', backref='class')
    
    #a car class can have many promotionssubcompacts
    promotionals = db.relationship('Promotional', backref='promo')
    
    #many-to-many relationship with Address
    place = db.relationship('Address', secondary=dropOff,
                            foreign_keys='[dropOff.c.classID, dropOff.c.toLocation]',
                            backref=db.backref('location', lazy='dynamic'),
                            overlaps="fromClass,fromLoc")
    
    
class Car(db.Model):
    __tablename__ = 'car'
    carID = db.Column(db.Integer, primary_key=True)
    carMake = db.Column(db.String(50), nullable=False)
    carModel = db.Column(db.String(50), nullable=False)
    yearMade = db.Column(db.Integer, nullable=False)
    carColor = db.Column(db.String(50), nullable=False)
    licensePlate = db.Column(db.String(50), nullable=False, unique=True)
    classID = db.Column(db.Integer, db.ForeignKey('carClass.carClassID'), nullable=False) 
    icon = db.Column(db.String(length=5000), nullable=True, unique=False)

class Promotional(db.Model):
    __tablename__ = 'promotional'
    promotionalID = db.Column(db.Integer, primary_key=True)
    classID = db.Column(db.Integer, db.ForeignKey('carClass.carClassID'), nullable=False)
    discountRate = db.Column(db.Integer, nullable=False)
    startPromoDate = db.Column(db.Date, nullable=False)
    endPromoDate = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    
    #a promotional may be applied to a car that is rented
    rents = db.relationship('Rent', backref='promo')
     
class Rent(db.Model):
    __tablename__ = 'rent'
    rentID = db.Column(db.Integer, primary_key=True)
    carID = db.Column(db.Integer, db.ForeignKey('car.carID'), nullable=False)
    locationRentedID = db.Column(db.Integer, db.ForeignKey('address.addressID'), nullable = False)
    locationDropOffID = db.Column(db.Integer, db.ForeignKey('address.addressID'), nullable = False)
    odometerRented = db.Column(db.Integer, nullable=False, default=50)
    odometerReturned = db.Column(db.Integer, nullable=False)
    gasVolume = db.Column(Enum('empty', 'quarter_full', 'half_full', 'three_quarters_full', 'full'), nullable=False)
    dateRented = db.Column(db.Date, nullable=False)
    dateReturned = db.Column(db.Date, nullable=False)
    requestedClass = db.Column(db.String(50), nullable=False)
    receivedClass = db.Column(db.String(50), nullable=False)
    promotionalID = db.Column(db.Integer, db.ForeignKey('promotional.promotionalID'), nullable=True)
    driverLicense = db.Column(db.Integer, db.ForeignKey('user.driverLicense'), nullable=False)
    
    #explicitly specify foreign key
    toAddress = db.relationship('Address', backref='rentsToAddress', foreign_keys='Rent.locationDropOffID')
    fromAddress = db.relationship('Address', backref='rentsFromAddress', foreign_keys='Rent.locationRentedID')
    
    
    
class User(db.Model,UserMixin):
    __tablename__ = 'user'
    driverLicense = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addressID = db.Column(db.Integer, db.ForeignKey('address.addressID'), nullable = False)
    passwordHash = db.Column(db.String(length=60),nullable=False)
    type = db.Column(Enum('customer','employee'), default='customer', nullable=False) 
    
    #a user can have many phone numbers
    userPhoneNumbers = db.relationship('PhoneNumber', backref='user_owner')
    
    #a user can request many rents
    rents = db.relationship('Rent', backref='renters')
    
    def checkPassword(self,attemptedPassword):
        userPass = User.query.filter_by(id=self.id).first()
        if userPass.passwordHash == attemptedPassword:
            return True
        return False
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.passwordHash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class PhoneNumber(db.Model):
    __tablename__ = 'phoneNumber'
    phoneNumberID = db.Column(db.Integer, primary_key=True)
    phoneNumbers = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.driverLicense'))
    
    
class Employee(User):
    __tablename__ = 'employee'
    driverLicense = db.Column(db.Integer, db.ForeignKey('user.driverLicense'), primary_key=True)
    locationAssignedID = db.Column(db.Integer, db.ForeignKey('address.addressID'), nullable=False)
    category = db.Column(Enum('worker','driver','manager','clerk','cleaner'), nullable=False)
    isPresident = db.Column(db.Boolean, nullable=False, default=False)
    isVicePresident = db.Column(db.Boolean, nullable=False, default=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'employee',
    }
    
    #explicitly specify foreign key
    assignedAddress = db.relationship('Address', backref='employeeLocations', foreign_keys='Employee.locationAssignedID')
    
    

class Customer(User):
    __tablename__ = 'customer'
    driverLicense = db.Column(db.Integer, db.ForeignKey('user.driverLicense'), primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }


    

    
    
    
    
    
    
