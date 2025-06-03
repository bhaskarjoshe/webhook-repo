import os

from flask import Flask

from app.extensions import init_mongo
from app.webhook.routes import webhook


# Creating our flask app
def create_app():

    template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
    static_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    init_mongo(app)

    # registering all the blueprints

    app.register_blueprint(webhook)

    return app
