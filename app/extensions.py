import os

from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo

from app.settings.logger import logger

load_dotenv()

# Setup MongoDB here
mongo = PyMongo()


def init_mongo(app: Flask):
    """Initialize MongoDB connection"""
    try:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")

        mongo.init_app(app, uri=mongo_uri)
        mongo.db.command("ping")
        logger.info("MongoDB connection established successfully")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {str(e)}")
        raise
    return mongo
