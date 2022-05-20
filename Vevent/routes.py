from flask import redirect, render_template, request, session, url_for

from Vevent import app, db
from Vevent.models import User
from Vevent.utils import load_user

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/events", methods=["POST"]) # check if authenticated
def events():
    email = request.form['email']
    password = request.form['password']
    user = load_user({"email": email, "password": password})
    if user:
        print(session)
        return render_template('events.html')
    elif not User.query.filter_by(email=email).first():
        new_user = User(
            email = email,
            password = password
        )
        db.session.add(new_user)
        print(new_user.email, new_user.password)
    return redirect(url_for('login'))

@app.route("/events/<id>") # check if authenticated
def event(id):
    return render_template('event.html')

@app.route("/create") # check if authenticated
def create():
    return render_template('create.html')

@app.route("/faq") # check if authenticated
def faq():
    return render_template('faq.html')