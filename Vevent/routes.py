import json, geocoder
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
        markers=[]
        for event in events_query_all:
            coords = get_coordinates(event.location)
            markers.append({
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': coords['lat'],
                'lng': coords['lng'],
                'infobox': event.name
            })
        current_location = geocoder.ip('me').latlng
        markers.append(
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': current_location[0],
                'lng': current_location[1],
                'infobox': "Current Location"
            }
        )
        return render_template('events.html',
            events=[{"name": event.name, "id": event._id} for event in events_query_all],
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

@app.route("/events/<id>")
def event(id):
    if not session['user']:
        flash("Not authenticated.")
        return redirect(url_for('login'))
    event = Event.query.filter_by(_id=id).first()
    user_accounts = json.loads(User.query.filter_by(email=session['user']).first().accounts)
    participant=""
    if event.conversation_id in user_accounts:
        participant=client.conversations.conversations(event.conversation_id).participants.get(user_accounts[event.conversation_id]).fetch()
    else:
        participant=client.conversations.conversations(event.conversation_id).participants.create(identity=session['user'])
        user_accounts[event.conversation_id]=participant.sid
        db.session.query(User).filter(User.email==session['user']).update(
            {User.accounts: json.dumps(user_accounts)}
        )
        db.session.commit()
    conversation = client.conversations.conversations(event.conversation_id).fetch()
    return render_template('event.html', data=event, conversation=conversation, participant=participant)

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