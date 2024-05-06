from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import StringField, SubmitField,IntegerField,FloatField,SelectField,HiddenField,BooleanField,PasswordField
from wtforms.validators import Length,DataRequired, EqualTo,ValidationError
from datetime import datetime
from flask import flash
import re

from static.entities import User

def CheckFormError(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} : {error}", category='error')
            
class LoginForm(FlaskForm):
    email=StringField(label='Email:',validators=[DataRequired()])
    password=PasswordField(label='Password:',validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

def validate_driverLicense(form, field):
    # Check if the driver's license follows the format ###-##-######
    license_number = field.data
    if not re.match(r'^[A-Za-z]\d{2}-\d{2}-\d{6}$', license_number):
        raise ValidationError('Invalid driver license format! Please enter a valid Philippine driver license number.')

def validate_email(form, field):
    email = field.data
    if '@' not in email:
        raise ValidationError('Invalid email format! Please enter a valid email address.')

def validate_unique_driverLicense(form, field):
    driver_license = field.data
    existing_user = User.query.filter_by(driverLicense=driver_license).first()
    if existing_user:
        raise ValidationError('Driver License already exists in the database!')
     
class UserForm(FlaskForm):
    driverLicense = StringField(label='Driver License:', validators=[Length(min=13, max=13), DataRequired(), validate_driverLicense, validate_unique_driverLicense])
    name = StringField(label='Full Name:', validators=[Length(min=2, max=200), DataRequired()])
    email = StringField(label='Email:', validators=[Length(min=2, max=200), DataRequired(), validate_email])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    address = SelectField(label='Address:', choices=[], validators=[DataRequired()])
    submit = SubmitField(label='Submit')
    
class AddressForm(FlaskForm):
    streetName = StringField(label='Street Name: ', validators=[Length(min=2,max=200), DataRequired()])
    streetNumber = StringField(label='Street Number: ', validators=[Length(min=2,max=200), DataRequired()])
    
    provincesPhilippines = [
    "Abra", "Agusan del Norte", "Agusan del Sur", "Aklan", "Albay", "Antique", "Apayao", "Aurora", "Basilan",
    "Bataan", "Batanes", "Batangas", "Benguet", "Biliran", "Bohol", "Bukidnon", "Bulacan", "Cagayan",
    "Camarines Norte", "Camarines Sur", "Camiguin", "Capiz", "Catanduanes", "Cavite", "Cebu", "Cotabato",
    "Davao de Oro", "Davao del Norte", "Davao del Sur", "Davao Occidental", "Davao Oriental", "Dinagat Islands",
    "Eastern Samar", "Guimaras", "Ifugao", "Ilocos Norte", "Ilocos Sur", "Iloilo", "Isabela", "Kalinga",
    "La Union", "Laguna", "Lanao del Norte", "Lanao del Sur", "Leyte", "Maguindanao del Norte", "Maguindanao del Sur",
    "Marinduque", "Masbate", "Misamis Occidental", "Misamis Oriental", "Mountain Province", "Negros Occidental",
    "Negros Oriental", "Northern Samar", "Nueva Ecija", "Nueva Vizcaya", "Occidental Mindoro", "Oriental Mindoro",
    "Palawan", "Pampanga", "Pangasinan", "Quezon", "Quirino", "Rizal", "Romblon", "Samar", "Sarangani", "Siquijor",
    "Sorsogon", "South Cotabato", "Southern Leyte", "Sultan Kudarat", "Sulu", "Surigao del Norte", "Surigao del Sur",
    "Tarlac", "Tawi-Tawi", "Zambales", "Zamboanga del Norte", "Zamboanga del Sur", "Zamboanga Sibugay", "Metro Manila"]
    province = SelectField(label='Province: ', choices=provincesPhilippines, validators=[DataRequired()])
    
    citiesPhilippines = [
    "Alaminos", "Angeles City", "Antipolo", "Bacolod", "Bacoor", "Bago", "Baguio", "Bais", "Balanga", "Baliwag",
    "Batac", "Batangas City", "Bayawan", "Baybay", "Bayugan", "Biñan", "Bislig", "Bogo", "Borongan", "Butuan",
    "Cabadbaran", "Cabanatuan", "Cabuyao", "Cadiz", "Cagayan de Oro", "Calaca", "Calamba", "Calapan", "Calbayog",
    "Caloocan", "Candon", "Canlaon", "Carcar", "Carmona", "Catbalogan", "Cauayan", "Cavite City", "Cebu City",
    "Cotabato City", "Dagupan", "Danao", "Dapitan", "Dasmariñas", "Davao City", "Digos", "Dipolog", "Dumaguete",
    "El Salvador", "Escalante", "Gapan", "General Santos", "General Trias", "Gingoog", "Guihulngan", "Himamaylan",
    "Ilagan", "Iligan", "Iloilo City", "Imus", "Iriga", "Isabela", "Kabankalan", "Kidapawan", "Koronadal",
    "La Carlota", "Lamitan", "Laoag", "Lapu-Lapu City", "Las Piñas", "Legazpi", "Ligao", "Lipa", "Lucena", "Maasin",
    "Mabalacat", "Makati", "Malabon", "Malaybalay", "Malolos", "Mandaluyong", "Mandaue", "Manila", "Marawi",
    "Marikina", "Masbate City", "Mati", "Meycauayan", "Muñoz", "Muntinlupa", "Naga", "Naga", "Navotas", "Olongapo",
    "Ormoc", "Oroquieta", "Ozamiz", "Pagadian", "Palayan", "Panabo", "Parañaque", "Pasay", "Pasig", "Passi",
    "Puerto Princesa", "Quezon City", "Roxas", "Sagay", "Samal", "San Carlos", "San Carlos", "San Fernando",
    "San Fernando", "San Jose", "San Jose del Monte", "San Juan", "San Pablo", "San Pedro", "Santa Rosa",
    "Santo Tomas", "Santiago", "Silay", "Sipalay", "Sorsogon City", "Surigao City", "Tabaco", "Tabuk", "Tacloban",
    "Tacurong", "Tagaytay", "Tagbilaran", "Taguig", "Tagum", "Talisay", "Talisay", "Tanauan", "Tandag", "Tangub",
    "Tanjay", "Tarlac City", "Tayabas", "Toledo", "Trece Martires", "Tuguegarao", "Urdaneta", "Valencia",
    "Valenzuela", "Victorias", "Vigan", "Zamboanga City"]
    city = SelectField(label='City: ', choices=citiesPhilippines, validators=[DataRequired()], id="city")
    
    postalCode = StringField(label='Postal Code: ', validators=[DataRequired(), Length(min=4, max=4)])
    
    submit = SubmitField(label='Submit')
    
class PhoneNumberForm(FlaskForm):
    phoneNumber = StringField(label='PhoneNumber: ', validators=[Length(min=11,max=11), DataRequired()])
    submit = SubmitField(label='Submit')
    
    
    
    