import pprint
import datetime
from pymongo import MongoClient


def initialize_databases():
    client = MongoClient()  # Default local host
    db = client.bovadaDB
    return client, db


def select_collection(db, sport='NBA'):
    if sport == 'NBA':
        return db.nba
    elif sport == 'NFL':
        return db.nfl
    elif sport == 'CFB':
        return db.cfb
    elif sport == 'CBB':
        return db.cbb
    elif sport == 'NHL':
        return db.nhl
    elif sport == 'MLB':
        return db.mlb
    else:
        return None  # Not configured yet


def add_game_to_database(game, db_collection):
    """
    :param game: recordtype of game information containing id, spreads, prices, etc.
    :param db_collection: collection in database to add to
    :return: results of attempt to add to collection
    """
    cur_time = datetime.datetime.utcnow()

    str_to_add = '.' + str(cur_time.day) + '.' + str(cur_time.hour)
    post_result = db_collection.update_one({'game_id': game.game_id},  # TODO: check if none instead of set on insert
                                           {'$setOnInsert': {'game_id': game.game_id,
                                                             'home_spread_init': game.home_spread,
                                                             'away_spread_init': game.away_spread,
                                                             'home_ml_init': game.home_ml,
                                                             'away_ml_init': game.away_ml,
                                                             'over_init': game.over,
                                                             'under_init': game.under},
                                            '$set': {'update_time': cur_time,
                                                     'home_spread_cur': game.home_spread,
                                                     'away_spread_cur': game.away_spread,
                                                     'home_ml_cur': game.home_ml,
                                                     'away_ml_cur': game.away_ml,
                                                     'over_cur': game.over,
                                                     'under_cur': game.under},
                                            '$push': {
                                                'home_spread' + str_to_add: [str(cur_time.minute), game.home_spread],
                                                'away_spread' + str_to_add: [str(cur_time.minute), game.away_spread],
                                                'home_ml' + str_to_add: [str(cur_time.minute), game.home_ml],
                                                'away_ml' + str_to_add: [str(cur_time.minute), game.away_ml],
                                                'over' + str_to_add: [str(cur_time.minute), game.over],
                                                'under' + str_to_add: [str(cur_time.minute), game.under]}
                                            }, upsert=True)

    return check_post_sucess(post_result)


def add_user_to_database(user, db_collection):
    post_result = db_collection.update_one({'email': user.email},
                                           {'$setOnInsert': {'email': user.email},
                                            '$set': {'password_hash': user.password_hash,
                                                     'favorites': user.favorites}
                                            }, upsert=True)

    return check_post_sucess(post_result)


def add_user_favorites(user, db_collection):
    post_result = db_collection.update_one({'email': user.email},
                                           {'$set': {'favorites': user.favorites},
                                            }, upsert=True)
    print post_result
    print type(post_result)
    return check_post_sucess(post_result)


def check_post_sucess(post_result):
    if post_result.modified_count == 0 and post_result.upserted_id is None:
        status = False
    else:
        status = True
    return status


def get_games_by_sport(db, sport):
    games = []
    collection = select_collection(db, sport)
    cursor = collection.find()
    if cursor.count() > 0:
        for game in collection.find():
            games.append(game)

    return games


def print_all_databases(client):
    cursor = client.list_databases()
    for db in cursor:
        print db


def print_all_collection_items(collection):
    for item in collection.find():
        pprint.pprint(item)


def print_all_db_collections(db):
    for collection in db.collection_names():
        pprint.pprint(collection)

# delete game with db.xxx.delete_many({})

# def remove_old_games(game_id_list):
#     # iterate over every document in db, and if not in current games remove to keep memory down  (FOR NOW)
#     for game in collection.find():
#         if game['game_id'] not in game_id_list:
#             # Delete the game from collection based on current cursor
#             pass
#     return
