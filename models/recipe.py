from models import db
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

# Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('recipes', lazy=True))
    ingredients = db.relationship('Ingredient', secondary='recipe_ingredients', backref=db.backref('recipes', lazy=True), lazy='dynamic')

    def __repr__(self):
        return f'<Recipe {self.title}>'


# Ingredient Model
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Ingredient {self.name}>'


# Junction table for the many-to-many relationship
class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    quantity = db.Column(db.String(50), nullable=True)  # Store quantity for each ingredient in recipe

    recipe = db.relationship('Recipe', backref=db.backref('recipe_ingredients', cascade='all, delete-orphan'))
    ingredient = db.relationship('Ingredient', backref=db.backref('recipe_ingredients', cascade='all, delete-orphan'))


class RecipeUser(db.Model):
    __tablename__ = 'recipe_user'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False, primary_key=True)

    # Define relationships
    user = db.relationship('User', backref=db.backref('user', lazy=True))
    recipe = db.relationship('Recipe', backref=db.backref('recipe', lazy=True))
    
    def __repr__(self):
        return f'<RecipeUser {self.user_id} - {self.recipe_id}>'