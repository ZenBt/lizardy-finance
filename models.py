from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
from app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=True)
    
    def __repr__(self) -> str:
        return f'User <Email: {self.email}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self
    
    def check_password(self, password):
        return check_password_hash(pwhash=self.password, password=password)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(30), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self) -> str:
        return f'Tag  <Category: {self.tag}>, <owner: {self.user_id}>'


class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    cost = db.Column(db.Integer)
    description = db.Column(db.String(400), nullable=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_time = db.Column(db.DateTime, default=date.today)
    
    def __repr__(self) -> str:
        return f'Expence <name: {self.name}>, <owner: {self.user_id}>'
