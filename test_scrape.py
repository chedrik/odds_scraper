from odds_scraper import *
from selenium import webdriver


#### TODOS ####
# TODO: Investigate webdrive / seleniium and why it sometimes fails.  How to switch webpages, closing it, etch
# TODO: Design MongoDB scheme, investigate between pymongo and mongoengine
# TODO: Write main looping function to iterate through games

# url_to_scrape = generate_url('NFL')
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# driver = webdriver.Chrome(options=options)
#
# #driver.implicitly_wait(.3)
# driver.get(url_to_scrape)
# big_soup = BeautifulSoup(driver.page_source, 'html.parser') #### THIS HAS THE STUFF!!!!
# next_events = big_soup.find_all('div', class_='next-events-bucket')
# grouped_events = big_soup.find_all('div', class_='grouped-events')

#########################################################################################
url_to_scrape = generate_url('NBA')
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options) # TODO Deal with path nastiness
driver.implicitly_wait(4)  # TODO: Trim this time
driver.get(url_to_scrape)
big_soup = BeautifulSoup(driver.page_source, 'html.parser') #### THIS HAS THE STUFF!!!!
game_containers = big_soup.find_all('section', class_='coupon-content more-info') # TODO: find out if this deals with live games
#########################################################################################




#game_containers[10].find('span', class_='period') # date and time
#game_containers[10].find_all('span', class_='name') # team names
game_containers[10].find_all('span', class_='bet-price') # all 6 bet prices
game_containers[10].find_all('span', class_='market-line bet-handicap') # spread
game_containers[10].find_all('span', class_='market-line bet-handicap both-handicaps') # over under #s

driver.close()
print big_soup.prettify()
# raw_data = requests.get(url_to_scrape)
# main_soup = BeautifulSoup(raw_data.text, 'html.parser')
# print main_soup.prettify()
#soup = main_soup.find_all('div', id='OddsGridModule_3')[0]



#
# game_lines = {}
# c = 0
# import time #for tic doc debug
# while c < 1000:
#     tic = time.clock()
#     get_cur_lines()
#     c += 1
#     '''
#     plt.plot(x,y)
#     print plt.get_backend()
#     plt.show()
#     y[0] += c
#     '''
#     'test123.xlsx'
#     save_lines('test123.xlsx', c)
#     print ( "Elapsed Time is", time.clock()-tic)
#     '''
#     if (c % 5 == 0):
#         workbook = xlsxwriter.Workbook('test123.xlsx')
#         wkst = workbook.add_worksheet('DataBackup')
#         wkst.set_column(0,16384,11)
#         merge_format = workbook.add_format({'align': 'center'})
#         g_c = 0
#         # TODO: DEAL WITH ADDING AFTER PREVIOUS GAMES
#         # TODO: CHECK IF g_c > # cols (dont overrun excel sheet)
#         for key in sorted(game_lines):
#             wkst.merge_range(0,g_c,0,g_c+2,None)
#             wkst.write(0,g_c,''.join(key),merge_format)
#
#             for j in range(len(game_lines[key][10][0])):
#                 wkst.write(j+1,g_c+1,game_lines[key][10][0][j])
#                 wkst.write(j+1,g_c+2,game_lines[key][10][1][j])
#
#             g_c += 3
#         workbook.close()
#         '''
#     sleep(60)
# '''
# workbook = xlsxwriter.Workbook('test123.xlsx')
# wkst = workbook.add_worksheet('DataBackup')
# wkst.set_column(0,16384,11)
# merge_format = workbook.add_format({'align': 'center'})
# g_c = 0
# # TODO: DEAL WITH ADDING AFTER PREVIOUS GAMES, CHECK IF g_c > # cols
# for key in game_lines:
#     wkst.merge_range(0,g_c,0,g_c+2,None)
#     wkst.write(0,g_c,''.join(key),merge_format)
#
#     for j in range(len(game_lines[key][10][0])):
#         wkst.write(j+1,g_c+1,game_lines[key][10][0][j])
#         wkst.write(j+1,g_c+2,game_lines[key][10][1][j])
#
#     g_c += 3
# workbook.close()
# '''