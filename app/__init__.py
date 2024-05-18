from flask import Flask
from app.config import Config, DeploymentConfig, TestConfig
from flask_sqlalchemy import SQLAlchemy # class gives api to database
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  
login_manager.login_message_category = 'info'

def create_app(config=DeploymentConfig):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config)

    # from app.blueprints import main
    # flaskApp.register_blueprint(main)
    # db.drop_all(flaskApp)
    # db.create_all(flaskApp)
    db.init_app(flaskApp) # initalise db
    login_manager.init_app(flaskApp) # initialise login_manager

    # if config==DeploymentConfig:
    #     from test_data import deployment_data
    #     db.drop_all()
    #     db.create_all()
    #     deployment_data()

    with flaskApp.app_context():
        # Import models after app context to avoid circular imports
        from app import models

        # Create database tables if needed
        if config == DeploymentConfig:
            from test_data import deployment_data
            db.drop_all()
            db.create_all()
            deployment_data()

        # Register blueprints
        from app.blueprints import main
        flaskApp.register_blueprint(main)
    
    return flaskApp
    
# from app import models