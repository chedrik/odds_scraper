from odds_scraper import *
from selenium import webdriver
from database import *
import time


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
        big_soup = BeautifulSoup(web_driver.page_source, 'html.parser')
        game_containers = big_soup.find_all('section',
                                            class_='coupon-content more-info')  # TODO: find out if this deals with live games
        retry_count += 1
        num_games = len(game_containers)
    return game_containers


def cleanup_web_interface(driver):
    driver.close()


def main_loop(database):
    web_driver = open_web_interface()
    game_containers = extract_game_containers(web_driver, 'NBA')
    for k in range(len(game_containers)):
        game = make_game_object(game_containers[k])
        result = add_game_to_database(game, select_collection(database, 'NBA'))
        string = 'Added ' + str(game.game_id) + ' at time: ' + str(datetime.datetime.now()) + ' with result: '
        print string
        print result
    print ' '
    cleanup_web_interface(web_driver)


if __name__ == '__main__':
    while True:
        client, db = initialize_databases()
        main_loop(db)
        time.sleep(300)