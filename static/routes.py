from static import app
from flask import render_template
import locale

@app.route('/')
@app.route('/main')
def index():
    return render_template('main.html')

@app.route("/login", methods=['GET','POST'])
def login():
    return render_template('login.html')