import os

from flask import Flask

from app.celery_app import init_celery
from app.extensions import init_mongo
from app.webhook.routes import webhook


# Creating our flask app
def create_app():

    template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
    static_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Initialize extensions
    init_mongo(app)
    init_celery(app)

    # registering all the blueprints

    app.register_blueprint(webhook)

    return app
