from Vevent import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

class Event(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)

    def __init__(self, value):
        self.value = value

db.create_all()
    