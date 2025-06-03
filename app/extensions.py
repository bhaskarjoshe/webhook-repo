import os

from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo

load_dotenv()

# Setup MongoDB here
mongo = PyMongo()


def init_mongo(app: Flask):
    try:
        mongo.init_app(app, uri=os.getenv("MONGO_URI"))
    except Exception as e:
        print("mongo db connection failed", e)
    return mongo
