import os, requests
from Vevent import login_manager
from Vevent.models import User

@login_manager.user_loader
def load_user(user):
    email=User.query.filter_by(email=user['email']).first()
    if email and User.query.filter_by(password=user['password']).first():
        return email

def get_coordinates(address_text):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json?address="
        + address_text
        + "&key="
        + os.environ['GOOGLEMAPS_KEY']
    ).json()
    if len(response['results']) > 0:
        return response["results"][0]["geometry"]["location"]
    return None