from flask import jsonify, redirect, render_template, request, session, url_for, flash

from Vevent import app, db
from Vevent.models import User, Event
from Vevent.utils import load_user

@app.route("/")
def login():
    session['user'] = None
    return render_template('login.html')

@app.route("/events", methods=["GET", "POST"]) # check if authenticated
def events():
    if request.method == "GET":
        flash("Not authenticated.")
        return redirect(url_for('login'))
    email = request.form['email']
    password = request.form['password']
    if not email or not password:
        flash("Please provide data.")
        return redirect(url_for('login'))
    user = load_user({"email": email, "password": password})
    if user:
        session['user'] = email
        return render_template('events.html', events=[{"value": event.value, "id": event._id} for event in Event.query.all()])
    elif not User.query.filter_by(email=email).first():
        new_user = User(
            email = email,
            password = password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created!")
        return redirect(url_for('login'))
    flash("Incorrect information.")
    return redirect(url_for('login'))

@app.route("/events/<id>") # check if authenticated
def event(id):
    if not session['user']:
        flash("Not authenticated.")
        return redirect(url_for('login'))
    return render_template('event.html')

@app.route("/create") # check if authenticated
def create():
    if not session['user']:
        flash("Not authenticated.")
        return redirect(url_for('login'))
    return render_template('create.html')

@app.route("/faq") # check if authenticated
def faq():
    if not session['user']:
        flash("Not authenticated.")
        return redirect(url_for('login'))
    return render_template('faq.html')