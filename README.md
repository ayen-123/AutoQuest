# AutoQuest

AutoQuest is a server-rendered web application for managing a car rental service. It provides searchable vehicle listings, a booking (rent) workflow with pickup/drop-off handling, promotions, user registration with role differentiation (customer / employee), and simple profile/phone management. The app is built with Flask and SQLAlchemy and uses WTForms for input validation; most of the UI is implemented as HTML templates with lightweight JavaScript where needed. The codebase is structured so the data model, forms, and routes are easy to find and extend.

## Technologies Used
- Python (Flask web framework)
- Flask-SQLAlchemy / SQLAlchemy (ORM & models) — static/entities.py
- Flask-Login (session-based user authentication)
- Flask-Bcrypt (password hashing used in models)
- Flask-WTF + WTForms (forms & validation) — static/forms.py
- Jinja2 templates (server-rendered UI) — static/templates/
- SQLite (default datastore: instance/main.db)
- HTML, CSS, minimal JavaScript (static/js/, static/images/)
- Optional: Flask-Admin integration (admin initialized in run.py / static/admin.py)

## Key Files & Where to Look
- run.py — app entrypoint (creates DB and runs server on port 8080)
- static/__init__.py — Flask app factory-like setup, DB and extensions
- static/entities.py — SQLAlchemy models (Car, CarClass, Rent, User, Address, Promotional, etc.)
- static/forms.py — WTForms definitions and validations
- static/routes.py — route handlers (shop, registerRent, signup, login, user profile, promos)
- instance/main.db — example SQLite database included in the repo
- static/templates/ — HTML templates used by the app
- static/static (or static/) — static assets (JS, images)

## Features
- Vehicle catalog & search
  - Search and filter cars by make, model, year, color, license plate, or class; shop view returns car objects and prices joined with CarClass.
- Car detail pages
  - Per-car information and associated class/price details are rendered on a dedicated car info page.
- Booking / Rent registration flow
  - Authenticated users can register a rent for a selected car (pickup/drop-off, odometer, gas level, rental dates); the Rent form validates odometer and dates.
- Promotions & promo selection
  - Promotional records are tied to car classes and filtered by rental dates; promos are selectable in the booking UI and applied to pricing calculations.
- Role-based users (customers vs employees)
  - create_user factory creates Customer or Employee instances based on verification codes; Employee records include assigned location and category.
- Profile & phone management
  - Users can update profile information and add/delete phone numbers; phone numbers are validated for format in routes/forms.
- Admin integration
  - Admin setup is initialized on startup (static/admin.py) for administrative tasks and interfaces.
- Server-side validation & protected routes
  - Forms are validated with WTForms and routes are protected with Flask-Login decorators (login_required).
- Small JSON endpoint(s)
  - Example JSON response for available promos (get_promos) to support dynamic client behavior.

## Process/Architecture
The application is arranged as a small Flask package inside `static/`. Models live in `static/entities.py`, forms in `static/forms.py`, and request handlers in `static/routes.py`. On startup `run.py` imports the app, ensures the database tables exist (db.create_all()) and initializes the admin integration. Request flow is typical of server-rendered Flask apps: a route handler queries models via SQLAlchemy, passes objects to Jinja2 templates, and returns rendered HTML. Authentication state is managed with Flask-Login and the user loader points at `entities.User`. Pricing logic and rental calculations are implemented in route-level helper functions (e.g., getPrice, calculateRentalPrice).

## How to run 
1. Clone the repository
   - git clone https://github.com/ayen-123/AutoQuest.git
   - cd AutoQuest

2. Create and activate a virtual environment
   - python -m venv .venv
   - source .venv/bin/activate   (Windows: .venv\Scripts\activate)

3. Install dependencies
   - python -m pip install --upgrade pip
   - pip install -r requirements.txt

4. Inspect / (optionally) remove the included SQLite DB
   - The repo contains an example DB at `instance/main.db`. If you want a fresh DB, remove or move that file before starting.

5. Start the app
   - python run.py
   - The server listens on 0.0.0.0:8080 by default. Open http://127.0.0.1:8080

   Notes:
   - On startup the app runs `db.create_all()` within the app context, creating tables if they do not exist.
   - `admin.init_app(app)` is called from run.py to set up the administrative interface if present.

6. Register and use the app
   - Use the "Register Address" then "Signup" flows to create users. Supplying certain verification codes (handled in entities.create_user) will create Employee accounts with specific categories/privileges.
   - Login at /login to access protected routes (shop, register rent, user pages).

7. Debugging & logs
   - The app is started with debug=True in run.py which enables auto-reload and traceback pages. For production, run with debug off and behind a WSGI server.




