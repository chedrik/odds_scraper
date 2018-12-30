from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db
from bson import ObjectId
from database import add_user_favorites
# TODO: do functions go above or below classes?
sports = ['NFL', 'CFB', 'NBA', 'CBB', 'Soccer', 'Hockey']


@login.user_loader
def load_user(id):
    user_from_db = db.users.find_one({'_id': ObjectId(id)})
    if user_from_db is not None:
        user = User(id=user_from_db['_id'], email=user_from_db['email'], password_hash=user_from_db['password_hash'])
    else:
        user = None  # TODO: if this fails, we should report 500 error
    return user


class User(UserMixin):

    def __init__(self, id=None, email=None, password_hash=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.favorites = {'sports': [], 'teams': []}  # TODO: implement favorites

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_favorite(self, items):
        for item in items:
            if item in sports:
                self.favorites['sports'].append(item)
            else:
                self.favorites['teams'].append(item)
        result = add_user_favorites(self, db.users)
        return result


# maybe include favorites here too?
