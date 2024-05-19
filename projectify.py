from flask_migrate import Migrate
from app import create_app, db
from app.config import DeploymentConfig

if __name__ == '__main__':
    flaskApp = create_app(DeploymentConfig)
    migrate = Migrate(flaskApp, db) # test should also be updated with new schema 
# # db.drop_all()
# # db.create_all()
# # import test_data
    flaskApp.run(debug=True) 