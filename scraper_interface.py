from scraper import *
from selenium import webdriver
from bs4 import BeautifulSoup
from database import *
from config import Config
import time


def open_web_interface():
    """
    Starts headless chrome interface.
    :return: selenium web driver object
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    if Config.GOOGLE_CHROME_BIN:  # for Heroku
        options.binary_location = Config.GOOGLE_CHROME_BIN
    prefs = {'profile.managed_default_content_settings.images': 2}  # Load without images
    options.add_experimental_option("prefs", prefs)
    web_driver = webdriver.Chrome(options=options)
    return web_driver


def extract_game_containers(web_driver, sport='NBA'):
    """
    Parse out info for a given sport and return a list of game htmls to parse further
    :param web_driver: selenium driver for navigating
    :param sport: sport name for generating correct URL to parse
    :return:  list of html where each item in list corresponds to a single game.
    """
    retry_count = 0
    num_games = 0
    game_containers = None
    while num_games == 0 and retry_count <= 10:
        url_to_scrape = generate_url(sport)
        web_driver.get(url_to_scrape)
        # web_driver.implicitly_wait(5)  # TODO: Trim/Extend this time
        big_soup = BeautifulSoup(web_driver.page_source, 'html.parser')
        game_containers = big_soup.find_all('section',
                                            class_='coupon-content more-info')
        retry_count += 1
        num_games = len(game_containers)
    return game_containers


def cleanup_web_interface(driver):
    """
    Close web interface to prevent resource use.
    :param driver: selenium web driver
    :return: void
    """
    driver.quit()


def fetch_all_odds(db):
    """
    Get odds of every sport and add them to appropriate collection in db
    :param db: pymongo database object
    :return: fault flag boolean whether process was a success
    """
    web_driver = open_web_interface()
    fault_flag = False
    for sport in Config.SUPPORTED_SPORTS:
        game_containers = extract_game_containers(web_driver, sport)
        print 'fetched ' + str(len(game_containers)) + ' ' + sport + ' games.'
        for k in range(len(game_containers)):
            if not check_game_in_progress(game_containers[k]):
                game = make_game_object(game_containers[k])
                result = add_game_to_database(game, select_collection(db, sport))
                team_rank_result = update_ranks(game, db.teams)
                if result is False:  # TODO: log to current_app.logger if this fails
                    fault_flag = True

    cleanup_web_interface(web_driver)
    return fault_flag


def main_test_loop(database, sport='CBB'):  # FOR TESTING ONLY
    web_driver = open_web_interface()
    game_containers = extract_game_containers(web_driver, sport)
    for k in range(len(game_containers)):
        if not check_game_in_progress(game_containers[k]):
            game = make_game_object(game_containers[k])
            result = add_game_to_database(game, select_collection(database, sport))
            string = 'Added ' + str(game.game_id) + ' at time: ' + str(datetime.datetime.now()) + ' with result: '
            print string
            print result
    print ' '
    cleanup_web_interface(web_driver)


if __name__ == '__main__':
    client, db = initialize_databases()
    while True:
        print 'fetching'
        fetch_all_odds(db)
        # main_test_loop(db)
        print 'waiting'
        time.sleep(120)
