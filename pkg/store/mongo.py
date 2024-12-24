import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from internal.config.logger import loggers

name = os.getenv("DB_USERNAME")
pwd = os.getenv("DB_PASSWORD")

uri = f"mongodb+srv://{name}:{pwd}@cluster0.thayz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    loggers.infoLog.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    loggers.errorLog.error(e)

db = client["messages_db"]


def NewMongoDB():
    return db
