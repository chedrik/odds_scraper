from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from app import login, db
from bson import ObjectId
import jwt
from time import time
from database import add_user_favorites, select_collection

sports = ['NFL', 'CFB', 'NBA', 'CBB', 'Soccer', 'Hockey']


@login.user_loader
def load_user(id):
    user_from_db = db.users.find_one({'_id': ObjectId(id)})
    if user_from_db is not None:
        user = User(id=user_from_db['_id'], email=user_from_db['email'],
                    password_hash=user_from_db['password_hash'], favorites=user_from_db['favorites'])
    else:
        user = None  # TODO: if this fails, we should report 500 error
    return user


def delete_user(id):
    return db.users.remove({'_id': ObjectId(id)})


class User(UserMixin):

    def __init__(self, id=None, email=None, password_hash=None, favorites=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.favorites_list = []
        if favorites is not None:
            self.favorites = favorites
            for item in favorites['sports']:
                self.favorites_list.append(item)
            for item in favorites['teams']:
                self.favorites_list.append(item)
        else:
            self.favorites = {'sports': [], 'teams': []}
            self.favorites_list = []

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': str(self.id), 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def add_favorite(self, items):
        not_added = []
        for item in items:
            if item in sports:
                if item not in self.favorites['sports']:
                    self.favorites['sports'].append(item)
                    self.favorites_list.append(item)
                else:
                    not_added.append(item)
            else:
                if item not in self.favorites['teams']:
                    self.favorites['teams'].append(item)
                    self.favorites_list.append(item)
                else:
                    not_added.append(item)
        result = add_user_favorites(self, db.users)
        return result, not_added

    def remove_favorites(self, items):  # TODO: HTML for this function
        for item in items:
            if item in sports:
                if item in self.favorites['sports']:
                    self.favorites['sports'].remove(item)
                    self.favorites_list.remove(item)
            else:
                if item in self.favorites['teams']:
                    self.favorites['teams'].remove(item)
                    self.favorites_list.remove(item)
        result = add_user_favorites(self, db.users)
        return result

    def get_all_favorites(self):
        favorites = []
        favorites_without_games = []
        for sport in self.favorites['sports']:
            collection = select_collection(db, sport)
            cursor = collection.find()
            if cursor.count() > 0:
                for game in collection.find():
                    favorites.append(game)
            else:
                favorites_without_games.append(sport)
        for team in self.favorites['teams']:
            # TODO: determine the sport of the team
            collection = select_collection(db, 'NBA')
            game_cursor = collection.find({'game_id': team}) # TODO: BUGFIX, doesnt find both teams, likely due to "find_one". Should iterate over cursor1
            if game_cursor.count() > 0:
                for game in collection.find({'game_id': team}):
                    favorites.append(game)
            else:
                favorites_without_games.append(team)

        return favorites, favorites_without_games

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:  # if token is expired or not valid it will return error
            return
        return load_user(id)