from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from database import initialize_databases
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(ENV='development')
login = LoginManager(app)
login.login_view = 'auth.login'
mail = Mail(app)
moment = Moment(app)
client, db = initialize_databases()

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

# exception logging
if app.config['MAIL_SERVER']:
    auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'], subject='Oops!',
        credentials=auth, secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/odds.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Started odds scraper')

from app import routes, models
