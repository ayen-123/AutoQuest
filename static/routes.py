from static import app

@app.route('/')
@app.route('/main')
#@login_required
def index():
    return "Hello World"