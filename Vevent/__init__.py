from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///element.sqlite"
db = SQLAlchemy(app)
db.create_all()

import Vevent.routes
