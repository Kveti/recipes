# app.py
from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import *  # Import db object
from routes.user_routes import user_bp
from routes.recipe_routes import recipe_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(recipe_bp)

@app.route('/')
def index():
    return "Welcome to the Flask App!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

# Route for logging out
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Dashboard - Only accessible by Admin and User
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    users = None
    if session['role'] == RoleEnum.ADMIN.value:
        users = User.query.all()
    
    recipes = Recipe.query.filter_by(user_id=session['user_id']).all()
    rus = RecipeUser.query.filter_by(user_id=session["user_id"]).all()
    for ru in rus:
        r = Recipe.query.get(ru.recipe_id)
        recipes.append(Recipe.query.get(ru.recipe_id))

    return render_template('dashboard.html', users=users, recipes=recipes)
    

if __name__ == '__main__':
    app.run(debug=True)

































#from flask import Flask, render_template, redirect, url_for, request, session, flash
#from flask_sqlalchemy import SQLAlchemy
#from models import db, User, Recipe, Ingredient, RecipeIngredient, RoleEnum
#from werkzeug.security import generate_password_hash, check_password_hash
#
#app = Flask(__name__)
#app.config['SECRET_KEY'] = 'your_secret_key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db.init_app(app)
#
## Route for the home page
#@app.route('/')
#def home():
#    #return redirect(url_for('dashboard'))
#    #return "Welcome to the Flask App!"
#    return render_template('welcome.html')
#
## Route for login page
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        username = request.form['username']
#        password = request.form['password']
#        
#        user = User.query.filter_by(username=username).first()
#        if user and check_password_hash(user.password, password):
#            session['user_id'] = user.id
#            session['username'] = user.username
#            session['role'] = user.role
#            flash('Login successful!', 'success')
#            return redirect(url_for('dashboard'))
#        else:
#            flash('Invalid credentials. Please try again.', 'danger')
#    
#    return render_template('login.html')
#
## Route for logging out
#@app.route('/logout')
#def logout():
#    session.clear()
#    flash('You have been logged out.', 'info')
#    return redirect(url_for('login'))
#
## Dashboard - Only accessible by Admin and User
#@app.route('/dashboard')
#def dashboard():
#    if 'user_id' not in session:
#        return redirect(url_for('login'))
#
#    if session['role'] == RoleEnum.ADMIN.value:
#        users = User.query.all()
#        recipes = Recipe.query.all()
#        return render_template('dashboard.html', users=users, recipes=recipes)
#    else:
#        recipes = Recipe.query.filter_by(user_id=session['user_id']).all()
#        return render_template('dashboard.html', recipes=recipes)
#
#
#
#
#
### Initialize the database
##@app.before_first_request
##def create_tables():
##    db.create_all()
#
#if __name__ == '__main__':
#    #db.create_all()
#    app.run(debug=True)
#
#
#
#
