from pymongo import MongoClient
import pprint
import datetime

# db_test = client.pymongo_test <-- has current nba from initall test
# collection = db_test.tester


def initialize_databases():
    client = MongoClient()  # Default local host
    db = client.bovadaDB
    return client, db


def select_collection(db, sport='NBA'):
    if sport == 'NBA':
        return db.nba
    else:
        return None  # Not configured yet


def add_game_to_database(game, db_collection):
    '''
    :param game: recordtype of game information containing id, spreads, prices, etc.
    :param db_collecton: collection in database to add to
    :return: results of attempt to add to collection
    '''
    cur_time = datetime.datetime.now()  # TODO: replace this with $currentDate, or smarter UTC time and convert to local time in flask front end implementation

    str_to_add = '.' + str(cur_time.day) + '.' + str(cur_time.hour)
    post_result = db_collection.update({'game_id': game.game_id},
                                    {'$set': {'update_time': cur_time, 'game_id': game.game_id},
                                     '$push': {'home_spread' + str_to_add: [str(cur_time.minute), game.home_spread],
                                               'away_spread' + str_to_add: [str(cur_time.minute), game.away_spread],
                                               'home_ml' + str_to_add: [str(cur_time.minute), game.home_ml],
                                               'away_ml' + str_to_add: [str(cur_time.minute), game.away_ml],
                                               'over' + str_to_add: [str(cur_time.minute), game.over],
                                               'under' + str_to_add: [str(cur_time.minute), game.under]}
                                     }, upsert=True)

    return post_result


def add_user_to_database(user, db_collection):
    post_result = db_collection.update({'email': user.email},
                                    {'$set': {'email': user.email,
                                              'password_hash': user.password_hash,
                                              'favorites': user.favorites},
                                     }, upsert=True)

    return post_result


def add_user_favorites(user, db_collection):
    post_result = db_collection.update({'email': user.email},
                                    {'$set': {'favorites': user.favorites},
                                     }, upsert=True)
    return post_result


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

# def remove_old_games(game_id_list):
#     # iterate over every document in db, and if not in current games remove to keep memory down  (FOR NOW)
#     for game in collection.find():
#         if game['game_id'] not in game_id_list:
#             # Delete the game from collection based on current cursor
#             pass
#     return

