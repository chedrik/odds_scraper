from flask import Flask
from config import Config
from flask_login import LoginManager
from database import initialize_databases

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(ENV='development')
login = LoginManager(app)
login.login_view = 'login'
client, db = initialize_databases()

from app import routes, models, errors
