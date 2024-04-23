from app import flaskApp

@flaskApp.route("/")
def groups():
    return "Test Page. Flask is working"

