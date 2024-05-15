from flask_migrate import Migrate
from app import create_app, db
from app.config import DeploymentConfig

if __name__ == '__main__':
    flaskApp = create_app(DeploymentConfig)
    migrate = Migrate(flaskApp, db) # test should also be updated with new schema 
    flaskApp.run(debug=True) 