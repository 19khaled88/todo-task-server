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


# client = MongoClient(
#     "mongodb+srv://khaled:VNHAybzMnVDF6NMq@cluster0.ka5da.mongodb.net/hrms?retryWrites=true&w=majority")
