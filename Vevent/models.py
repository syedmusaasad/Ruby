from flask_login import UserMixin

from Vevent import db

class User(UserMixin, db.Model):
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)

    def __init__(self, email, password):
        self.email = email
        self.password = password

class Event(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    email = db.Column(db.String)
    location = db.Column(db.String)

    def __init__(self, value, email, location):
        self.value = value
        self.email = email
        self.location = location

db.create_all()
    