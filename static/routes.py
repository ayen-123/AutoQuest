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
    loginForm = LoginForm()
    return render_template('login.html', loginForm=loginForm)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    userForm = UserForm()
    addressForm = AddressForm()
    phoneNumberForm = PhoneNumberForm()
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
            db.session.add(address_to_create)
            db.session.commit()  # Commit the Address object to get the generated addressID

            if userForm.validate_on_submit():
                # Create the User object using the generated addressID
                print("User form is valid")
                user_to_create = User(
                    driverLicense=userForm.driverLicense.data,
                    name=userForm.name.data,
                    email=userForm.email.data,
                    addressID=address_to_create.addressID,  # Use the generated addressID
                    passwordHash=userForm.password1.data
                )
                db.session.add(user_to_create)
                db.session.commit()

                if phoneNumberForm.validate_on_submit():
                    # Create the PhoneNumber object using the generated driverLicense
                    print("Phone Number form is valid")
                    phone_to_create = PhoneNumber(
                        phoneNumbers = phoneNumberForm.phoneNumber.data,
                        owner = user_to_create.driverLicense # Use the generated driverLicense
                    )
                    db.session.add(phone_to_create)
                    db.session.commit()
                    flash(f'Success! User has been created!', category='success')
                    return redirect(url_for('login'))
                else:
                    print("Phone Number Form is invalid")
                    CheckFormError(phoneNumberForm)
            else:
                print("User form is invalid")
                CheckFormError(userForm)     
        else:
            print("Address form is invalid")
            CheckFormError(addressForm)          
    else:
        print("GET Method, Rendering signup template")
    return render_template('signup.html', userForm=userForm, addressForm=addressForm, phoneNumberForm=phoneNumberForm)




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