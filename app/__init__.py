from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy # class gives api to database
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'  
login_manager.login_message_category = 'info'

def create_app(config):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config)

    from app.blueprints import main
    flaskApp.register_blueprint(main)
    # db.drop_all(flaskApp)
    # db.create_all(flaskApp)
    db.init_app(flaskApp) # initalise db 
    login_manager.init_app(flaskApp) # initialise login_manager
    
    return flaskApp
    
from app import models