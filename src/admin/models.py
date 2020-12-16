from src import db,login_manager
from datetime import datetime
from flask_login import UserMixin
import json



@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile = db.Column(db.String(80), unique=False, nullable=False,default='profile.jpg')
    access=db.Column(db.String(20), unique=False, nullable=True,default='Full')
    is_admin =db.Column(db.Boolean, nullable=False,default=True)
    is_confirm=db.Column(db.Boolean, nullable=False,default=False)


    def __repr__(self):
        return '<User %r>' % self.username


db.create_all()