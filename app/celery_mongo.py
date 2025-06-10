import os

from flask_pymongo import PyMongo

from app.settings.logger import logger

celery_mongo = PyMongo()


def init_celery_mongo():
    """Initialize MongoDB connection for Celery tasks"""
    try:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")

        from flask import Flask

        app = Flask(__name__)
        app.config["MONGO_URI"] = mongo_uri

        celery_mongo.init_app(app)
        celery_mongo.db.command("ping")
        logger.info("Celery MongoDB connection established successfully")
    except Exception as e:
        logger.error(f"Celery MongoDB connection failed: {str(e)}")
        raise
    return celery_mongo
