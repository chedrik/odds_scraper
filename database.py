from pymongo import MongoClient
import pprint
import time # For testing
import datetime
client = MongoClient()  # Default local host
db = client.bovadaDB
nba_collection = db.nba

db_test = client.pymongo_test
collection = db_test.tester

# cursor = client.list_databases()
# for db in cursor:
#     print db


def add_to_database(game, db_collecton=collection):  # TODO: Split by hour? or by more than that?  Need to optimize for performance
    cur_time = datetime.datetime.now()
    disp_cur_time = cur_time.ctime()  #TODO: replace this with $currentDate

    #if collection.find({"game_id" : game.game_id}) is not None:
    str_to_add = '.' + str(cur_time.day) + '.' + str(cur_time.hour)
    post_result = db_collecton.update({'game_id': game.game_id},
                                    {'$set': {'update_time': cur_time, 'game_id': game.game_id},
                                     '$push': {'home_spread' + str_to_add: [str(cur_time.minute), game.home_spread],
                                               'away_spread' + str_to_add: [str(cur_time.minute), game.away_spread],
                                               'home_ml' + str_to_add: [str(cur_time.minute), game.home_ml],
                                               'away_ml' + str_to_add: [str(cur_time.minute), game.away_ml],
                                               'over' + str_to_add: [str(cur_time.minute), game.over],
                                               'under' + str_to_add: [str(cur_time.minute), game.under]}
                                     }, upsert=True)

    return


# def remove_old_games(game_id_list):
#     # iterate over every document in db, and if not in current games remove to keep memory down  (FOR NOW)
#     for game in collection.find():
#         if game['game_id'] not in game_id_list:
#             # Delete the game from collection based on current cursor
#             pass
#     return


# for x in (collection.find()):
#     pprint.pprint(x)
