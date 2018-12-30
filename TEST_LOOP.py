from database import *
from odds_scraper import *
from selenium import webdriver

count = 0
while count < 50:
    url_to_scrape = generate_url('NBA')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)  # TODO Deal with path nastiness
    driver.implicitly_wait(5)  # TODO: Trim/Extend this time
    retry_count = 0
    num_games = 0  # TODO: smarter dealing with this
    while (num_games == 0 and retry_count <= 10):
        driver.implicitly_wait(1)  # TODO: Trim/Extend this time
        driver.get(url_to_scrape)
        big_soup = BeautifulSoup(driver.page_source, 'html.parser')  #### THIS HAS THE STUFF!!!!
        game_containers = big_soup.find_all('section',
                                            class_='coupon-content more-info')  # TODO: find out if this deals with live games
        retry_count += 1
        num_games = len(game_containers)
    if retry_count > 10:
        print 'WE DONE FAILED, NO GAMES'
    driver.close()
    for k in range(len(game_containers)):
        game = make_game_object(game_containers[k])
        add_game_to_database(game)
        string = 'Added to db: ' + str(game.game_id)
        print string
    time.sleep(300)
    count += 1
for x in (collection.find()):
    pprint.pprint(x)