from pymongo import MongoClient
from settings import (
    MONGODB_HOST,
    MONGODB_PORT,
    MONGODB_USERNAME,
    MONGODB_PASSWORD,
    MONGODB_DATABASE_NAME,
    MONGODB_MOVIES_COLLECTION_NAME,
)


def get_movies_collection():
    return get_database()[MONGODB_MOVIES_COLLECTION_NAME]


def get_database():
    client = MongoClient(MONGODB_HOST, MONGODB_PORT, username=MONGODB_USERNAME, password=MONGODB_PASSWORD)
    return client[MONGODB_DATABASE_NAME]
