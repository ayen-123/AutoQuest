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
    loginForm = LoginForm
    return render_template('login.html', loginForm=loginForm)

@app.route("/signup", methods=['GET','POST'])
def signup():
    signupForm = SignupForm
    return render_template('signup.html', signupForm=SignupForm)

@app.route('/', methods=['GET', 'POST'])
def RegisterAddress():
    addressForm = AddressForm()
    userForm = UserForm()
    if addressForm.validate_on_submit():
        streetName = addressForm.streetName.data
        streetNumber = addressForm.streetNumber.data
        city = addressForm.city.data
        province = addressForm.province.data
        postalCode = addressForm.postalCode.data
        
        newAddress = Address(streetName=streetName, streetNumber=streetNumber, city=city, province=province, postalCode=postalCode)
        
        similarAddress = Address.query.filter(Address.fullAddressName == newAddress.fullAddressName).all()
        if similarAddress:
            flash('Address is already in the database!', category='warning')
            return redirect(url_for('index'))
        else: 
            db.session.add(newAddress)
            db.session.commit()
            flash(f'Success! Your address has been added!', category='success')
            return render_template('login.html', userForm=userForm, addressForm=addressForm)
    else:
        CheckFormError(addressForm)
        return render_template('login.html', userForm=userForm, addressForm=addressForm)



@app.route('/', methods=['GET', 'POST'])
def CreateUser():
    userForm = UserForm()
    addresses = Address.query.all()
    userForm.address.choices = [(address.addressID, address.fullAddressName) for address in addresses]

    if userForm.validate_on_submit():
        user_to_create = User(
            driverLicense=userForm.driverLicense.data,
            addressID=userForm.address.data,
            name=userForm.name.data,
            passwordHash=userForm.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        flash('Success! User has been created!', category='success')
        # Redirect to another page after successful form submission
        return redirect(url_for('login'))

    else:
        # Display form validation errors
        CheckFormError(userForm)

    addressForm = AddressForm
    return render_template('login.html', userForm=userForm, addressForm=addressForm)

@app.route('/shop', methods=['GET','POST'])
def Shop():
    car_type = request.args.get('type')
    if car_type:
        carsWithClass = db.session.query(Car, CarClass.price).join(CarClass).filter(CarClass.type == car_type).all()
    else:
        carsWithClass = db.session.query(Car, CarClass.price).join(CarClass).all()
    results = [{'car': car, 'price': price} for car, price in carsWithClass]
    return render_template('shop.html', cars=results, car_type=car_type)
# def Shop():
#     carsWithClass = db.session.query(Car, CarClass.price).join(CarClass).all()
#     results = [{'car': car, 'price': price} for car, price in carsWithClass]
#     return render_template('shop.html', cars=results)


@app.route('/car_info/<int:car_id>', methods=['GET','POST'])
def CarInfo(car_id):
    car = Car.query.get(car_id)  # Fetch the car using the car_id
    car_class = CarClass.query.get(car.classID) # Access the CarClass associated with the car object
    # Render the CarInfo.html template with the fetched information
    return render_template('CarInfo.html', car=car, car_class=car_class)