from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import StringField, SubmitField,IntegerField,FloatField,SelectField,HiddenField,BooleanField,PasswordField
from wtforms.validators import Length,DataRequired, EqualTo,ValidationError
from datetime import datetime
import re

class LoginForm(FlaskForm):
    name=StringField(label='Name:',validators=[DataRequired()])
    password=PasswordField(label='Password:',validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class UserForm(FlaskForm):
    def validate_driverLicense(form, field):
        # Check if the driver's license follows the format ###-##-######
        license_number = field.data
        if not re.match(r'^\d{3}-\d{2}-\d{6}$', license_number):
            raise ValidationError('Invalid driver license format. Please enter a valid Philippine driver license number.')

    driverLicense = StringField(label='Driver License:', validators=[Length(min=13,max=13), DataRequired(), validate_driverLicense])
    name = StringField(label='Full Name:', validators=[Length(min=2,max=200), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'),DataRequired()])
    address = SelectField(label='Address:', coerce=int, choices=[])
    submit = SubmitField(label='Submit')
    
class AddressForm(FlaskForm):
    streetName = StringField(label='Street Name: ', validators=[Length(min=2,max=200), DataRequired()])
    streetNumber = StringField(label='Street Number: ', validators=[Length(min=2,max=200), DataRequired()])
    
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
    city = SelectField(label='City: ', choices=citiesPhilippines, validators=[DataRequired()])
    
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
    
    postalCode = StringField(label='Postal Code: ', validators=[DataRequired(), Length(min=4, max=4)])
    
    submit = SubmitField(label='Submit')
    
    