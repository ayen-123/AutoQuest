from static import app
from flask import render_template
import locale

@app.route('/')
@app.route('/main')
#@login_required
def index():
    return render_template('main.html')