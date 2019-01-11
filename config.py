import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fake_key'
    FAVORITES =['NFL',
                'CFB',
                'NBA',
                'CBB',
                'Soccer',
                'Hockey',
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
                'Washington Wizards']

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['gambling.odds@gmail.com']
    #DB_URI = os.environ.get('DATABASE_URL') or os.path.join(basedir, 'app.db')
    # TODO: clean out venv and then requirements.txt
