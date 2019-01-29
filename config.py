import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fake_key'
    FAVORITES = ['NFL',
                 'CFB',
                 'NBA',
                 'CBB',
                 'Soccer',
                 'NHL',
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
                 'Winnipeg Jets']

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['gambling.odds@gmail.com']

    SUPPORTED_SPORTS = ['NBA', 'NHL']
    # DB_URI = os.environ.get('DATABASE_URL') or os.path.join(basedir, 'app.db')
