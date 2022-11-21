from mongoengine import connect
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv('DATABASE_URL')


def get_db(db_name='hrms'):
    client = MongoClient(URI)
    db = client.get_database(db_name)

    return db
