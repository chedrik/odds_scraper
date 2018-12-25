from odds_scraper import *
from selenium import webdriver
from database import *

def open_web_interface():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    web_driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)  # TODO Deal with path nastiness
    return web_driver


def extract_game_containers(web_driver, sport='NBA'):
    retry_count = 0
    num_games = 0
    while num_games == 0 and retry_count <= 10:
        url_to_scrape = generate_url(sport)
        web_driver.get(url_to_scrape)
        web_driver.implicitly_wait(5)  # TODO: Trim/Extend this time
        game_containers = big_soup.find_all('section',
                                            class_='coupon-content more-info')  # TODO: find out if this deals with live games
        retry_count += 1
        num_games = len(game_containers)
    return game_containers


def cleanup_web_interface(driver):
    driver.close()


def main_loop(game_containers, sport='NBA'):
    for k in range(len(game_containers)):
        game = make_game_object(game_containers[k])
        # TODO: dynamically choose selection here, test main loop functionality.  set if name == __main__ stuff
        add_to_database(game, collection)
        string = 'Added to db: ' + str(game.game_id)
        print string
    time.sleep(300)
