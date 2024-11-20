from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Define the User Role Enum
class RoleEnum(Enum):
    USER = 'user'
    ADMIN = 'admin'


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    #name = db.Column(db.String(60), nullable=True)
    #surname = db.Column(db.String(60), nullable=True)
    #nickname = db.Column(db.String(60), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default=RoleEnum.USER)
    
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hashes the password before storing it."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifies if the password is correct."""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)


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
    quantity = db.Column(db.String(50), nullable=True)  # Store quantity for each recipe-ingredient relation

    recipe = db.relationship('Recipe', backref=db.backref('recipe_ingredients', cascade='all, delete-orphan'))
    ingredient = db.relationship('Ingredient', backref=db.backref('recipe_ingredients', cascade='all, delete-orphan'))



