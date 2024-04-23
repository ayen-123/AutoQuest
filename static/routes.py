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
    userForm = UserForm()
    addressForm = AddressForm()
    return render_template('login.html', userForm=userForm, addressForm=addressForm)

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

        