from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy # class gives api to database
from flask_migrate import Migrate

flaskApp = Flask(__name__)
flaskApp.config.from_object(Config)
db = SQLAlchemy(flaskApp)
migrate = Migrate(flaskApp, db)

from app import routes, model 