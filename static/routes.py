from static import app
from flask import render_template
from static.entities import  *
import locale


@app.route('/')
@app.route('/main')
def index():
    return render_template('main.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/shop', methods=['GET','POST'])
def Shop():
    carsWithClass = db.session.query(Car, CarClass.price).join(CarClass).all()
    results = [{'car': car, 'price': price} for car, price in carsWithClass]
    return render_template('Shop.html', cars=results)