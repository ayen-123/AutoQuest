from sqlalchemy import desc
from static import app, db
from flask import render_template, redirect, url_for, request,flash, get_flashed_messages
from static.entities import *
import locale
from datetime import datetime
from static.forms import *
from flask_login import current_user, login_user,logout_user,login_required

def CheckFormError(form):
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')
            
@app.route('/')
@app.route('/main')
def index():
    return render_template('main.html')

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.checkPassword(attemptedPassword=form.password.data):
            login_user(attempted_user) 
            flash(f'Success. You are logged in as: {attempted_user.name}', category='success')
            return redirect(url_for('Shop'))
        else:
            flash('Email and password does not exist in the database!',category='danger')
    return render_template('login.html', form=form)

@app.route("/registerAddress", methods=['GET','POST'])
def registerAddress():
    addressForm = AddressForm()
    print(f"Request method: {request.method}")
    
    if request.method == 'POST':
        print("Form data received:")
        print(addressForm.data)
        
        if addressForm.validate_on_submit():
            print("Address form is valid")
            address_to_create = Address(
                streetName=addressForm.streetName.data,
                streetNumber=addressForm.streetNumber.data,
                city=addressForm.city.data,
                province=addressForm.province.data,
                postalCode=addressForm.postalCode.data
            )
            similarAddress = Address.query.filter(Address.fullAddressName == address_to_create.fullAddressName).all()
            if similarAddress:
                flash(f'Address {address_to_create.fullAddressName} is already in the database!',category='warning')
                return redirect(url_for('index'))
            else:
                db.session.add(address_to_create)
                db.session.commit()  # Commit the Address object to get the generated addressID
                flash(f'Success! Address {address_to_create.fullAddressName} has been saved!', category='success')
                return redirect(url_for('signup', address_id = address_to_create.addressID))
                
        else:
            print("Address form is invalid")
            CheckFormError(addressForm)          
    else:
        print("GET Method, Rendering signup template")
    return render_template('registerAddress.html', addressForm=addressForm)
    

@app.route("/signup/<int:address_id>", methods=['GET', 'POST'])
def signup(address_id):
    userForm = UserForm()
    print(f"Request method: {request.method}")
    
    userAddress = Address.query.filter_by(addressID=address_id).first()
    userForm.address.choices = [(userAddress.addressID, f'{userAddress.fullAddressName}')]
    
    if request.method == 'POST':
        print("Form data received:")
        print(userForm.data)
        
        if userForm.validate_on_submit():
            print("User form is valid")
            user_to_create = User(
                driverLicense=userForm.driverLicense.data,
                name=userForm.name.data,
                email=userForm.email.data,
                addressID=userForm.address.data,  
                passwordHash=userForm.password1.data,
                type='customer',
            )
            db.session.add(user_to_create)
            db.session.commit()
            flash(f'Success! User has been created!', category='success')
            return redirect(url_for('login'))
        else:
            print("User form is invalid")
            CheckFormError(userForm)
             
    else:
        print("GET Method, Rendering signup template")
    return render_template('signup.html', userForm=userForm, address_id = userAddress.addressID)



@app.route('/shop', methods=['GET','POST'])
@login_required
def Shop():
    car_type = request.args.get('type')
    if car_type:
        carsWithClass = db.session.query(Car, CarClass.price).join(CarClass).filter(CarClass.type == car_type).all()
    else:
        carsWithClass = db.session.query(Car, CarClass.price).join(CarClass).all()
    results = [{'car': car, 'price': price} for car, price in carsWithClass]
    return render_template('shop.html', cars=results, car_type=car_type)


@app.route('/car_info/<int:car_id>', methods=['GET','POST'])
@login_required
def CarInfo(car_id):
    car = Car.query.get(car_id)  # Fetch the car using the car_id
    car_class = CarClass.query.get(car.classID) # Access the CarClass associated with the car object
    # Render the CarInfo.html template with the fetched information
    return render_template('CarInfo.html', car=car, car_class=car_class)

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('index'))