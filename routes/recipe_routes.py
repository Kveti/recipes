from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from models import * #db, Recipe, Ingredient, RecipeIngredient
from werkzeug.security import generate_password_hash, check_password_hash

recipe_bp = Blueprint('recipe_bp', __name__)

# Route for the home page
@recipe_bp.route('/')
def home():
    return redirect(url_for('dashboard'))

@recipe_bp.route('/recipes')
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



@recipe_bp.route('/recipe/<int:id>', methods=['GET'])
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


@recipe_bp.route('/recipe/edit/<int:id>', methods=['GET', 'POST'])
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

@recipe_bp.route('/recipe/add', methods=['GET', 'POST'])
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

        return redirect(url_for('recipe_bp.recipe_add'))  # Redirect back to the same page (or you can redirect elsewhere)

    return render_template('recipe_add.html')

# Route to delete a recipe
@recipe_bp.route('/recipe/delete/<int:id>', methods=['POST'])
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    recipe = Recipe.query.get_or_404(id)
    if recipe.user_id == session['user_id'] or session['role'] == RoleEnum.ADMIN.value:

        

        rus = RecipeUser.query.filter_by(recipe_id=id).all()
        for ru in rus:
            db.session.delete(ru)
            db.session.commit()

        db.session.delete(recipe)
        db.session.commit()

        flash('Recipe deleted successfully!', 'danger')
    else:
        flash('You are not authorized to delete this recipe.', 'warning')
    
    return redirect(url_for('dashboard'))
