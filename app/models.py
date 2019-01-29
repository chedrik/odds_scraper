from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
import jwt
from bson import ObjectId
from app import login, db
from database import add_user_favorites, select_collection, get_games_by_sport

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
    current_app.logger.info('Deleted user: ' + id)
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
        current_app.logger.info(self.email + ' added favorites')
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
        current_app.logger.info(self.email + ' removed favorites')
        return result

    def get_all_favorites(self):
        favorites = []
        favorites_without_games = []
        for sport in self.favorites['sports']:
            games = get_games_by_sport(db, sport)
            if len(games) == 0:
                favorites_without_games.append(sport)
            else:
                for game in games:
                    if game not in favorites:  # Don't double add games if game fav + team fav
                            favorites.append(game)
        for team in self.favorites['teams']:
            # TODO: determine the sport of the team
            collection = select_collection(db, 'NBA')
            game_cursor = collection.find({'game_id': team})
            if game_cursor.count() > 0:
                for game in collection.find({'game_id': team}):
                    if game not in favorites:
                        favorites.append(game)
            else:
                favorites_without_games.append(team)

        favorites.sort(key=lambda x: x['game_id'][0])  # time order
        return favorites, favorites_without_games

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:  # if token is expired or not valid it will return error
            return None
        return load_user(id)
