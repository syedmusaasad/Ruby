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
    name = db.Column(db.String)
    email = db.Column(db.String)
    location = db.Column(db.String)
    datetime = db.Column(db.DateTime)
    organization = db.Column(db.String)
    cost = db.Column(db.String)
    description = db.Column(db.String)
    objective = db.Column(db.String)

    def __init__(self, name, email, location, datetime, organization, cost, description, objective):
        self.name = name
        self.email = email
        self.location = location
        self.datetime = datetime
        self.organization = organization
        self.cost = cost
        self.description = description
        self.objective = objective

db.create_all()
    