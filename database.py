import pprint
import datetime
from pymongo import MongoClient
from config import Config


def initialize_databases(uri=None):
    """
    Creates DB and client objects.
    :return: pymongo client and bovada database
    """
    if uri is None:
        client = MongoClient()
    else:
        client = MongoClient(Config.MONGODB_URI,
                             connectTimeoutMS=30000,
                             socketTimeoutMS=None,
                             socketKeepAlive=True)  # Default local host
    db = client.bovadaDB
    return client, db


def select_collection(db, sport='NBA'):
    """
    Gets collection name based on required sport.
    :param db: bovada db object
    :param sport: sport name
    :return: pymongo collection for required sport
    """
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


def check_steam(game, db_collection):
    """
    Checks whether the odds have changed since last update.  If the odds change more than once in Config.STEAM_THRESHOLD,
    the steam flag is set.  There is a debounce time off of LINE_CHANGE_THRESHOLD, so a changed line will show up as a
    new change for that amount of time before being set to false
    :param game: recordtype of game information containing id, spreads, prices, etc.
    :param db_collection: collection in database to add to
    :return: list for each item of [time, changed_bool]
    """
    cur_time = datetime.datetime.utcnow()
    game_db = db_collection.find_one({'game_id': game.game_id})
    steam = False
    if game_db is None or 'change_vector' not in game_db:  # New game, no steam
        return [[datetime.datetime.min, False], [datetime.datetime.min, False], [datetime.datetime.min, False],
                [datetime.datetime.min, False], [datetime.datetime.min, False], [datetime.datetime.min, False]], steam
    else:
        change_vector = game_db['change_vector']

    if game_db['home_spread_cur'] != game.home_spread:
        if (cur_time - change_vector[0][0]).seconds < Config.STEAM_THRESHOLD:
            steam = True
        change_vector[0] = [cur_time, True]
    elif (cur_time - change_vector[0][0]).seconds > Config.LINE_CHANGE_THRESHOLD:
        change_vector[0][1] = False
    if game_db['away_spread_cur'] != game.away_spread:
        if (cur_time - change_vector[1][0]).seconds < Config.STEAM_THRESHOLD:
            steam = True
        change_vector[1] = [cur_time, True]
    elif (cur_time - change_vector[1][0]).seconds > Config.LINE_CHANGE_THRESHOLD:
        change_vector[1][1] = False
    if game_db['home_ml_cur'] != game.home_ml:
        if (cur_time - change_vector[2][0]).seconds < Config.STEAM_THRESHOLD:
            steam = True
        change_vector[2] = [cur_time, True]
    elif (cur_time - change_vector[2][0]).seconds > Config.LINE_CHANGE_THRESHOLD:
        change_vector[2][1] = False
    if game_db['away_ml_cur'] != game.away_ml:
        if (cur_time - change_vector[3][0]).seconds < Config.STEAM_THRESHOLD:
            steam = True
        change_vector[3] = [cur_time, True]
    elif (cur_time - change_vector[3][0]).seconds > Config.LINE_CHANGE_THRESHOLD:
        change_vector[3][1] = False
    if game_db['over_cur'] != game.over:
        if (cur_time - change_vector[4][0]).seconds < Config.STEAM_THRESHOLD:
            steam = True
        change_vector[4] = [cur_time, True]
    elif (cur_time - change_vector[4][0]).seconds > Config.LINE_CHANGE_THRESHOLD:
        change_vector[4][1] = False
    if game_db['under_cur'] != game.under:
        if (cur_time - change_vector[5][0]).seconds < Config.STEAM_THRESHOLD:
            steam = True
        change_vector[5] = [cur_time, True]
    elif (cur_time - change_vector[5][0]).seconds > Config.LINE_CHANGE_THRESHOLD:
        change_vector[5][1] = False
    return change_vector, steam


def add_game_to_database(game, db_collection):
    """
    :param game: recordtype of game information containing id, spreads, prices, etc.
    :param db_collection: collection in database to add to
    :return: results of attempt to add to collection
    """
    cur_time = datetime.datetime.utcnow()

    str_to_add = '.' + str(cur_time.day) + '.' + str(cur_time.hour)
    change_vector, steam = check_steam(game, db_collection)
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
                                                     'under_cur': game.under,
                                                     'change_vector': change_vector,
                                                     'steam': steam},
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
    """
    Adds or updates user object to user database for tracking favorites, etc.
    :param user: User object as defined in app/models.py
    :param db_collection: pymongo collection for holding website users
    :return: boolean of whether collection update was successful.
    """
    post_result = db_collection.update_one({'email': user.email},
                                           {'$setOnInsert': {'email': user.email},
                                            '$set': {'password_hash': user.password_hash,
                                                     'favorites': user.favorites}
                                            }, upsert=True)

    return check_post_sucess(post_result)


def add_team_to_database(team, db_collection):
    """
    Helper fcn to initialize teams in database
    :param team: list of name, sport
    :param db_collection: pymongo collection for holding teams and info
    :return: boolean of whether collection update was successful.
    """
    if team[1] in ['CFB', 'CBB']:
        post_result = db_collection.insert_one({'team': team[0], 'sport': team[1], 'ranking': ''})
    else:
        post_result = db_collection.insert_one({'team': team[0], 'sport': team[1]})

    return post_result


def update_ranks(game, db_collection):
    """
    Updates the rank for teams in college
    :param game: recordtype of game information containing id, spreads, prices, etc.
    :param db_collection: pymongo collection for holding teams and info
    :return: boolean of whether collection update was successful.  If not in college, returns None
    """
    if get_team_sport(game.game_id[1], db_collection) in ['CFB', 'CBB']:
        home_result = db_collection.update_one({'team': game.game_id[1]},
                                               {'$set': {'rank': game.home_rank}})

        away_result = db_collection.update_one({'team': game.game_id[2]},
                                               {'$set': {'rank': game.away_rank}})

        return check_post_sucess(home_result) and check_post_sucess(away_result)
    else:
        return None


def get_team_sport(team, db_collection):
    team_db = db_collection.find_one({'team': team})
    if team_db is None:
        # current_app.logger.warning('No sport found for ' + team) TODO: log this
        return None
    else:
        return team_db['sport']


def add_user_favorites(user, db_collection):
    """
    Updates the favorites for a given user.
    :param user: User object as defined in app/models.py
    :param db_collection: pymongo collection for holding website users
    :return: boolean of whether collection update was successful.
    """
    post_result = db_collection.update_one({'email': user.email},
                                           {'$set': {'favorites': user.favorites},
                                            }, upsert=True)
    print post_result
    print type(post_result)
    return check_post_sucess(post_result)


def check_post_sucess(post_result):
    """
    Generic database update check, which returns true if new item is added OR item is modified
    :param post_result: pymongo post result
    :return: boolean for successful db change
    """
    if post_result.modified_count == 0 and post_result.upserted_id is None:
        status = False
    else:
        status = True
    return status


def get_games_by_sport(db, sport):
    """
    Fetches all database posts for a given sport
    :param db: pymongo db object
    :param sport: string sport name
    :return: list of game objects fetched from database
    """
    games = []
    collection = select_collection(db, sport)
    cursor = collection.find()
    if cursor.count() > 0:
        for game in collection.find():
            games.append(game)
    games.sort(key=lambda x: x['game_id'][0] or datetime.datetime.max, reverse=True)  # time order
    return games


def get_steam_games(db):
    """
    Gets all games that have odds that have been changed, or that are currently being steamed
    :param db: bovada db object
    :return: list of game objects for changed games, and steam games
    """

    def reset_old_game_steam(game, collection):
        change_vector = game['change_vector']
        for k in range(6):
            change_vector[k][1] = False
        collection.update_one({'game_id': game['game_id']}, {'$set': {"steam": False,
                                                                      "change_vector": change_vector}})

    changed_games, steam_games = [], []
    for sport in Config.SUPPORTED_SPORTS:
        collection = select_collection(db, sport)
        changed_cursor = collection.find({"change_vector": True})
        if changed_cursor.count() > 0:
            for game in changed_cursor:
                if game['game_id'][0] is not None and datetime.datetime.now() < game['game_id'][0]:
                    reset_old_game_steam(game, collection)
                else:
                    changed_games.append(game)
        steam_cursor = collection.find({"steam": True})
        if steam_cursor.count() > 0:
            for game in steam_cursor:
                if game['game_id'][0] is not None and datetime.datetime.now() < game['game_id'][0]:
                    reset_old_game_steam(game, collection)
                else:
                    steam_games.append(game)

    return changed_games, steam_games


def remove_old_games(db, sport):
    # delete games that havent been updated in 1+ days
    collection = select_collection(db, sport)
    cursor = collection.find()
    del_count = 0
    if cursor.count() > 0:
        for game in collection.find():
            if game['game_id'][0] is not None and (datetime.datetime.utcnow() - game['game_id'][0]).days >= 1:
                del_ob = collection.delete_one({'game_id': game['game_id']})
                del_count += del_ob.deleted_count
    return del_count


def print_all_databases(client):
    """
    Helper fcn for debugging, prints all databases in pymongo client
    :param client: pymongo client object
    :return: void
    """
    cursor = client.list_databases()
    for db in cursor:
        print db


def print_all_collection_items(collection):
    """
    Helper fcn for debugging, prints all posts in a db
    :param collection: pymongo collection
    :return: void
    """
    for item in collection.find():
        pprint.pprint(item)


def print_all_db_collections(db):
    """
    Helper fcn for debugging, prints all collections in a db.
    :param db: pymongo db object
    :return: void
    """
    for collection in db.collection_names():
        pprint.pprint(collection)

# delete game with db.xxx.delete_many({})
