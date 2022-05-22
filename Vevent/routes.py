import json, geocoder
import math
from flask import redirect, render_template, request, session, url_for, flash
from flask_googlemaps import Map
from datetime import datetime as dt

from Vevent import app, db, client
from Vevent.models import User, Event
from Vevent.utils import get_coordinates, load_user

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
        events_query_all = Event.query.all()
        current_location = geocoder.ip('me').latlng
        markers=[]
        events=[]
        for event in events_query_all:
            coords = get_coordinates(event.location)
            markers.append({
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': coords['lat'],
                'lng': coords['lng'],
                'infobox': event.name
            })
            events.append(
                {
                    'name': event.name,
                    'id': event._id,
                    'description': event.description,
                    'cost': event.cost,
                    'dist': math.sqrt( ((current_location[0]-coords['lat'])**2)+((current_location[1]-coords['lng'])**2) )
                }
            )
        markers.append(
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': current_location[0],
                'lng': current_location[1],
                'infobox': "Current Location"
            }
        )
        events.sort(key=lambda event: event['dist'])
        return render_template('events.html',
            events=events,
            map=Map(identifier="Event_Map", lat=current_location[0], lng=current_location[1], markers=markers)
        )
    email = request.form['email']
    password = request.form['password']
    if not email or not password:
        flash("Please provide data.")
        return redirect(url_for('login'))
    user = load_user({"email": email, "password": password})
    if user:
        session['user'] = email
        return redirect(url_for('events'))
    elif not User.query.filter_by(email=email).first():
        new_user = User(
            email = email,
            password = password,
            accounts=json.dumps({})
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created!")
        return redirect(url_for('login'))
    flash("Incorrect information.")
    return redirect(url_for('login'))

@app.route("/events/<id>", methods=['GET', 'POST'])
def event(id):
    event = Event.query.filter_by(_id=id).first()
    if request.method == 'POST':
        text = request.form['text']
        if not text:
            flash("Please enter a message.")
            return redirect('/events/'+id)
        client.conversations.conversations(event.conversation_id).messages.create(author=session['user'], body=text)
        return redirect('/events/'+id)
    if not session['user']:
        flash("Not authenticated.")
        return redirect(url_for('login'))
    messages = client.conversations.conversations(event.conversation_id).messages.list(limit=20)
    return render_template('event.html', data=event, messages=messages)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        if not session['user']:
            flash("Not authenticated.")
            return redirect(url_for('login'))
        return render_template('create.html')
    name = request.form['name']
    location = request.form['location']
    if not get_coordinates(location):
        flash("Please re-enter address.")
        return redirect(url_for('create'))
    datetime = request.form['datetime']
    organization = request.form['organization']
    cost = request.form['cost']
    description = request.form['description']
    objective = request.form['objective']
    if not name or not location or not datetime or not organization or not cost or not description or not objective:
        flash("Please provide data.")
        return redirect(url_for('create'))
    conversation = client.conversations.conversations.create(friendly_name=name)
    new_event = Event(
        conversation_id=conversation.sid,
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
    return redirect(url_for('events'))

@app.route("/faq")
def faq():
    if not session['user']:
        flash("Not authenticated.")
        return redirect(url_for('login'))
    return render_template('faq.html')