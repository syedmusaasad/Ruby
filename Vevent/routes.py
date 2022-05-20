from flask import render_template, request, jsonify, make_response
import json

from Vevent import app, db
from Vevent.models import element

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/events")
def events():
    return render_template('events.html')

@app.route("/events/<id>")
def event(id):
    return render_template('event.html')

@app.route("/create")
def create():
    return render_template('create.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return make_response(jsonify([elmnt.value for elmnt in element.query.all()]), 200)
    else:
        db.session.add(element(json.loads(request.data)["task"]))
        db.session.commit()
        print([elmnt.value for elmnt in element.query.all()])
        return make_response(jsonify([elmnt.value for elmnt in element.query.all()]), 200)


@app.route("/<id>", methods=["DELETE", "PUT"])
def task(id):
    if request.method == "DELETE":
        element.query.filter_by(_id=id).delete()
        db.session.query(element).filter(element._id > id).update(
            {element._id: element._id - 1})
        db.session.commit()
        return make_response(jsonify([elmnt.value for elmnt in element.query.all()]), 200)
    else:
        db.session.query(element).filter(element._id == id).update(
            {element.value: json.loads(request.data)["value"]})
        db.session.commit()
        return make_response(jsonify([elmnt.value for elmnt in element.query.all()]), 200)