from odds_scraper import *
from selenium import webdriver
from database import *
from config import Config
import time


def open_web_interface():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    prefs = {'profile.managed_default_content_settings.images': 2}  # Load without images
    options.add_experimental_option("prefs", prefs)
    web_driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)  # TODO Deal with path nastiness
    return web_driver


def extract_game_containers(web_driver, sport='NBA'):
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
    driver.quit()


def fetch_all_odds(db):
    web_driver = open_web_interface()
    fault_flag = False
    for sport in Config.SUPPORTED_SPORTS:
        game_containers = extract_game_containers(web_driver, sport)
        for k in range(len(game_containers)):
            if not check_game_in_progress(game_containers[k]):
                game = make_game_object(game_containers[k])
                result = add_game_to_database(game, select_collection(db, sport))
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
