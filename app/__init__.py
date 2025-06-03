from flask import Flask

from app.extensions import init_mongo
from app.webhook.routes import webhook


# Creating our flask app
def create_app():

    app = Flask(__name__)

    init_mongo(app)

    # registering all the blueprints

    app.register_blueprint(webhook)

    return app
