from Vevent import login_manager
from Vevent.models import User

@login_manager.user_loader
def load_user(user):
    if User.query.filter_by(email=user['email']).first() and User.query.filter_by(password=user['password']).first():
        return User.query.filter_by(email=user['email']).first()