from models import db
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

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
