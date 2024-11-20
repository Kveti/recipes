# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Initialize the db instance here to be used in other models
db = SQLAlchemy()

# Import all models
from models.user import User, RoleEnum
from models.recipe import Recipe, Ingredient, RecipeIngredient, RecipeUser