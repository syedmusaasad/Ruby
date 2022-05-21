from flask import redirect, render_template, request, session, url_for, flash
from flask_googlemaps import Map
from datetime import datetime as dt

from Vevent import app, db
from Vevent.models import User, Event
from Vevent.utils import load_user

@app.route("/")
def login():
    session['user'] = None
    return render_template('login.html')

@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "GET":
        if not session['user']:
            flash("Not authenticated.")
            return redirect(url_for('login'))
        return render_template('events.html',
            events=[{"name": event.name, "id": event._id} for event in Event.query.all()],
            map=Map(identifier="Event_Map", lat=40, lng=-75)
            )
    email = request.form['email']
    password = request.form['password']
    if not email or not password:
        flash("Please provide data.")
        return redirect(url_for('login'))
    user = load_user({"email": email, "password": password})
    if user:
        session['user'] = email
        return render_template('events.html',
            events=[{"name": event.name, "id": event._id} for event in Event.query.all()],
            map=Map(identifier="Event_Map", lat=40, lng=-75)
            )
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

@app.route("/events/<id>")
def event(id):
    if not session['user']:
        flash("Not authenticated.")
        return redirect(url_for('login'))
    return render_template('event.html', data=Event.query.filter_by(_id=id).first())

@app.route("/create", methods=["GET", "POST"]) # make sure all fields are valid before committing to db
def create():
    if request.method == "GET":
        if not session['user']:
            flash("Not authenticated.")
            return redirect(url_for('login'))
        return render_template('create.html')
    name = request.form['name']
    location = request.form['location']
    datetime = request.form['datetime']
    organization = request.form['organization']
    cost = request.form['cost']
    description = request.form['description']
    objective = request.form['objective']
    if not name or not location or not datetime or not organization or not cost or not description or not objective:
        flash("Please provide data.")
        return redirect(url_for('create'))
    new_event = Event(
        name=name,
        email=session['user'],
        location=location,
        datetime=dt.strptime(datetime, '%Y-%m-%dT%H:%M'),
        organization=organization,
        cost=cost,
        description=description,
        objective=objective
    )
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('events')) # do not pass data, it's already handled

@app.route("/faq")
def faq():
    if not session['user']:
        flash("Not authenticated.")
        return redirect(url_for('login'))
    return render_template('faq.html')