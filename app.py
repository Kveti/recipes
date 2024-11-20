from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Recipe, Ingredient, RecipeIngredient, RoleEnum
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Route for the home page
@app.route('/')
def home():
    return redirect(url_for('dashboard'))

# Route for login page
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

    if session['role'] == RoleEnum.ADMIN.value:
        users = User.query.all()
        recipes = Recipe.query.all()
        return render_template('dashboard.html', users=users, recipes=recipes)
    else:
        recipes = Recipe.query.filter_by(user_id=session['user_id']).all()
        return render_template('dashboard.html', recipes=recipes)



@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    ret = "User ID: " + str(session["user_id"]) + "<br/>"
    ret = ret + "Role   : " + session["role"] + "<br/>"

    if session['role'] == RoleEnum.ADMIN.value:
        ret = ret + "ano som rola admin"
    else:
        ret = ret + "nie som rola adnim"

    return ret

    if session['role'] == RoleEnum.ADMIN.value:
        users = User.query.all()
        recipes = Recipe.query.all()
        return render_template('dashboard.html', users=users, recipes=recipes)
    else:
        recipes = Recipe.query.filter_by(user_id=session['user_id']).all()
        return render_template('dashboard.html', recipes=recipes)



@app.route('/recipe/<int:id>', methods=['GET'])
def recipe_show(id=None):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if id:
        recipe = Recipe.query.get(id)

        recipeIngredients = RecipeIngredient.query.filter_by(recipe_id=recipe.id)
        ing = []
        for ri in recipeIngredients:
            ingredient = Ingredient.query.get(ri.ingredient_id)
            ing.append(ingredient.name)

        return render_template('recipe_show.html', title = recipe.title, ins = recipe.instructions, ingredients = ing)
    else:
        ret = "nenasiel som id"
        print(ret)
        return redirect(url_for("dashboard"))
   #    recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, user_id=session['user_id'])
   #    db.session.add(recipe)
   #
   #db.session.commit()
   #flash('Recipe saved successfully!', 'success')
   #return redirect(url_for('dashboard'))

   #recipe = Recipe.query.get(id) if id else None
   #return render_template('recipe_form.html', recipe=recipe)


@app.route('/recipe/edit/<int:id>', methods=['GET', 'POST'])
def recipe_edit(id=None):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        if id:
            recipe = Recipe.query.get(id)
            recipe.title = title
            recipe.ingredients = ingredients
            recipe.instructions = instructions
        else:
            recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, user_id=session['user_id'])
            db.session.add(recipe)

        db.session.commit()
        flash('Recipe saved successfully!', 'success')
        return redirect(url_for(f'recipe/{id}'))

    recipe = Recipe.query.get(id) if id else None
    return render_template('recipe_form.html', recipe=recipe)

@app.route('/recipe/add', methods=['GET', 'POST'])
def recipe_add():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session["user_id"]
    print(user_id)

    if request.method == 'POST':
        # Get the recipe title
        title = request.form['title']
        instructions = request.form['instructions']

        # Get the ingredients from the form
        ingredients = request.form.getlist('ingredients[]')  # This gives a list of ingredients

        # Create a new recipe
        recipe = Recipe(title=title, instructions=instructions, user_id=session["user_id"])

        # Loop through ingredients and add them to the recipe
        for ingredient_name in ingredients:
            # Check if the ingredient already exists in the database
            ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
            if not ingredient:
                # If ingredient doesn't exist, create a new one
                ingredient = Ingredient(name=ingredient_name)
                db.session.add(ingredient)
            # Add the ingredient to the recipe's ingredients
            recipe.ingredients.append(ingredient)

        # Add the recipe to the session and commit to the database
        db.session.add(recipe)
        db.session.commit()

        return redirect(url_for('recipe_add'))  # Redirect back to the same page (or you can redirect elsewhere)

    return render_template('recipe_add.html')

# Route to delete a recipe
@app.route('/recipe/delete/<int:id>', methods=['POST'])
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    recipe = Recipe.query.get_or_404(id)
    if recipe.user_id == session['user_id'] or session['role'] == RoleEnum.ADMIN.value:
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted successfully!', 'danger')
    else:
        flash('You are not authorized to delete this recipe.', 'warning')
    
    return redirect(url_for('dashboard'))

# Route for admin to manage users
@app.route('/admin/users')
def manage_users():
    if 'user_id' not in session or session['role'] != RoleEnum.ADMIN.value:
        return redirect(url_for('login'))
    
    users = User.query.all()
    return render_template('dashboard.html', users=users)




@app.route('/users/add', methods=['GET', 'POST'])
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
            return redirect(url_for('add_user'))

        # Create new user
        new_user = User(username=username, role=role)
        new_user.set_password(password)

        try:
            # Add to the database
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('add_user'))  # Redirect to user add page or dashboard
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('add_user'))
    
    return render_template('add_user.html')




## Initialize the database
#@app.before_first_request
#def create_tables():
#    db.create_all()

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)