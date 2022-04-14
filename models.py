from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import app

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=True)
    
    def __repr__(self) -> str:
        return f'User N.{self.id} <Email: {self.email}>, <Password: {self.password}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self
    
    def check_password(self, password):
        return check_password_hash(pwhash=self.password, password=password)
    

