"""
This file is for handling MongoDB database connections based on
configuration stored in .env variable.
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_db():
    """
    get_db() : This function retrieves the mongo_uri and db name from
    .env variables, creates a MongoDB client, and returns database object.

    Returns:
    - database: database object that allows interaction with the specified database.
    """
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB_NAME")
    client = MongoClient(mongo_uri)
    database = client[mongo_db_name]

    return database
