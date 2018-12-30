import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fake_key'
    FAVORITES = [(0,0), (1,1), (2,2), (3,3), (4,4)]
    #DB_URI = os.environ.get('DATABASE_URL') or os.path.join(basedir, 'app.db')

