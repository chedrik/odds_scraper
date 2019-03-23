import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fake_key'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    MONGODB_URI = os.environ.get('MONGODB_URI') or None
    CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH') or '/usr/local/bin/chromedriver'
    GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN') or None
    FETCH_TIME = os.environ.get('FETCH_TIME') or 300.0

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['gambling.odds@gmail.com']

    SUPPORTED_SPORTS = ['NBA', 'NHL', 'MLB']
    STEAM_THRESHOLD = float(os.environ.get('STEAM_THRESHOLD') or 45*60)  # seconds for datetime delta
    LINE_CHANGE_THRESHOLD = float(os.environ.get('LINE_CHANGE_THRESHOLD') or 10000*60)  # seconds
    # DB_URI = os.environ.get('DATABASE_URL') or os.path.join(basedir, 'app.db')

    # Plot options
    MARKER_SIZE = 10
    COLORS = [u'#7f0000', u'#b30000', u'#d7301f', u'#ef6548', u'#fc8d59', u'#fdbb84', u'#fdd49e', u'#252525',
              u'#c6dbef', u'#9ecae1', u'#6baed6', u'#4292c6', u'#2171b5', u'#08519c', u'#08306b']
    # reds = bokeh.palettes.OrRd[9][:7]
    # blues = bokeh.palettes.Blues[9][:7]
    # blues.reverse()  # most intense should be the best odds
    # even = bokeh.palettes.Greys[9][1]
    # colors = reds + [even] + blues  # 15 different colors

    FAVORITES = ['NFL',
                 'NBA',
                 'MLB',
                 'NHL',
                 'CFB',
                 'CBB',
                 'Soccer',
                 'Atlanta Hawks',
                 'Boston Celtics',
                 'Brooklyn Nets',
                 'Charlotte Hornets',
                 'Chicago Bulls',
                 'Cleveland Cavaliers',
                 'Dallas Mavericks',
                 'Denver Nuggets',
                 'Detroit Pistons',
                 'Golden State Warriors',
                 'Houston Rockets',
                 'Indiana Pacers',
                 'Los Angeles Clippers',
                 'Los Angeles Lakers',
                 'Memphis Grizzlies',
                 'Miami Heat',
                 'Milwaukee Bucks',
                 'Minnesota Timberwolves',
                 'New Orleans Pelicans',
                 'New York Knicks',
                 'Oklahoma City Thunder',
                 'Orlando Magic',
                 'Philadelphia 76ers',
                 'Phoenix Suns',
                 'Portland Trail Blazers',
                 'Sacramento Kings',
                 'San Antonio Spurs',
                 'Toronto Raptors',
                 'Utah Jazz',
                 'Washington Wizards',
                 'Anaheim Ducks',
                 'Arizona Coyotes',
                 'Boston Bruins',
                 'Buffalo Sabres',
                 'Calgary Flames',
                 'Carolina Hurricanes',
                 'Chicago Blackhawks',
                 'Colorado Avalanche',
                 'Columbus Blue Jackets',
                 'Dallas Stars',
                 'Detroit Red Wings',
                 'Edmonton Oilers',
                 'Florida Panthers',
                 'Los Angeles Kings',
                 'Minnesota Wild',
                 'Montreal Canadiens',
                 'Nashville Predators',
                 'New Jersey Devils',
                 'New York Islanders',
                 'New York Rangers',
                 'Ottawa Senators',
                 'Philadelphia Flyers',
                 'Pittsburgh Penguins',
                 'San Jose Sharks',
                 'St. Louis Blues',
                 'Tampa Bay Lightning',
                 'Toronto Maple Leafs',
                 'Vancouver Canucks',
                 'Vegas Golden Knights',
                 'Washington Capitals',
                 'Winnipeg Jets',
                 'Atlanta Braves',
                 'Miami Marlins',
                 'New York Mets',
                 'Philadelphia Phillies',
                 'Washington Nationals',
                 'Chicago Cubs',
                 'Cincinnati Reds',
                 'Milwaukee Brewers',
                 'Pittsburgh Pirates',
                 'St. Louis Cardinals',
                 'Arizona Diamondbacks',
                 'Colorado Rockies',
                 'Los Angeles Dodgers',
                 'San Diego Padres',
                 'San Francisco Giants',
                 'Baltimore Orioles',
                 'Boston Red Sox',
                 'New York Yankees',
                 'Tampa Bay Rays',
                 'Toronto Blue Jays',
                 'Chicago White Sox',
                 'Cleveland Indians',
                 'Detroit Tigers',
                 'Kansas City Royals',
                 'Minnesota Twins',
                 'Houston Astros',
                 'Los Angeles Angels',
                 'Oakland Athletics',
                 'Seattle Mariners',
                 'Texas Rangers',
                 'Boston College',
                 'Clemson',
                 'Duke',
                 'Florida State',
                 'Georgia Tech',
                 'Louisville',
                 'Miami Florida',
                 'NC State',
                 'North Carolina',
                 'Pittsburgh',
                 'Syracuse',
                 'Virginia',
                 'Virginia Tech',
                 'Wake Forest',
                 'Cincinnati',
                 'East Carolina',
                 'Houston',
                 'Memphis',
                 'Navy',
                 'SMU',
                 'Temple',
                 'Tulane',
                 'Tulsa',
                 'UConn',
                 'UCF',
                 'USF',
                 'Baylor',
                 'Iowa State',
                 'Kansas',
                 'Kansas State',
                 'Oklahoma',
                 'Oklahoma State',
                 'TCU',
                 'Texas',
                 'Texas Tech',
                 'West Virginia',
                 'Illinois',
                 'Indiana',
                 'Iowa',
                 'Maryland',
                 'Michigan',
                 'Michigan State',
                 'Minnesota',
                 'Nebraska',
                 'Northwestern',
                 'Ohio State',
                 'Penn State',
                 'Purdue',
                 'Rutgers',
                 'Wisconsin',
                 'Charlotte',
                 'Florida Atlantic',
                 'Florida International',
                 'Louisina Tech',
                 'Marshall',
                 'Mid Tennessee State',
                 'North Texas',
                 'Old Dominion',
                 'Rice',
                 'Southern Miss',
                 'UTEP',
                 'UTSA',
                 'Western Kentucky',
                 'Akron',
                 'Ball State',
                 'Bowling Green',
                 'Buffalo',
                 'Central Michigan',
                 'Eastern Michigan',
                 'Kent State',
                 'Miami (OH)',
                 'Northern Illinois',
                 'Ohio',
                 'Toledo',
                 'Western Michigan',
                 'Air Force',
                 'Boise State',
                 'Colorado State',
                 'Fresno State',
                 'Hawaii',
                 'Nevada',
                 'New Mexico',
                 'San Diego State',
                 'San Jose State',
                 'UNLV',
                 'Utah State',
                 'Wyoming',
                 'Arizona',
                 'Arizona State',
                 'California',
                 'Colorado',
                 'Oregon',
                 'Oregon State',
                 'Stanford',
                 'UCLA',
                 'USC',
                 'Utah',
                 'Washington',
                 'Washington State',
                 'Alabama',
                 'Arkansas',
                 'Auburn',
                 'Florida',
                 'Georgia',
                 'Kentucky',
                 'LSU',
                 'Mississippi State',
                 'Missouri',
                 'Ole Miss',
                 'South Carolina',
                 'Tennessee',
                 'Texas A&M',
                 'Vanderbilt',
                 'Appalachian State',
                 'Arkansas State',
                 'Georgia Southern',
                 'Georgia State',
                 'Idaho',
                 'New Mexico State',
                 'Southern Alabama',
                 'Texas State',
                 'Troy',
                 'UL Lafayette',
                 'UL Monroe',
                 'Army',
                 'BYU',
                 'Liberty',
                 'Notre Dame',
                 'UMass']
