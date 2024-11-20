from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from models import * #db, User, RoleEnum
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user_bp', __name__)

## Dashboard - Only accessible by Admin and User
#@user_bp.route('/dashboard')
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


# Route for admin to manage users
@user_bp.route('/admin/users')
def manage_users():
    if 'user_id' not in session or session['role'] != RoleEnum.ADMIN.value:
        return redirect(url_for('login'))
    
    users = User.query.all()
    return render_template('dashboard.html', users=users)




@user_bp.route('/users/add', methods=['GET', 'POST'])
def add_user():
    #db.drop_all()  # This will drop all tables
    #db.create_all()  # Create the tables again
    
    if request.method == 'POST':
        # Get user data from the form
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # Optional: role defaults to 'user'

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('user_bp.add_user'))

        # Create new user
        new_user = User(username=username, role=role)
        new_user.set_password(password)

        try:
            # Add to the database
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('user_bp.add_user'))  # Redirect to user add page or dashboard
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('user_bp.add_user'))
    
    return render_template('add_user.html')

