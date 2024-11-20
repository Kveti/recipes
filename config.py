# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cms.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

#app.config['SECRET_KEY'] = 'your_secret_key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False