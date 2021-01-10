from unittest import TestCase
from unittest.mock import patch, MagicMock
from settings import (
    MONGODB_HOST,
    MONGODB_PORT,
    MONGODB_USERNAME,
    MONGODB_PASSWORD,
    MONGODB_DATABASE_NAME,
    MONGODB_MOVIES_COLLECTION_NAME,
)
from database import get_database, get_movies_collection


MODULE = "database"


class DatabaseTestCase(TestCase):

    @patch(f"{MODULE}.MongoClient")
    def test_get_database(self, MongoClient):
        client_mock = MagicMock()
        database_mock = MagicMock()

        def client_side_effect(key):
            return database_mock if key == MONGODB_DATABASE_NAME else None

        client_mock.__getitem__.side_effect = client_side_effect

        MongoClient.return_value = client_mock

        returned_database = get_database()

        MongoClient.assert_called_once_with(
            MONGODB_HOST,
            MONGODB_PORT,
            username=MONGODB_USERNAME,
            password=MONGODB_PASSWORD,
        )

        assert returned_database is database_mock

    @patch(f"{MODULE}.get_database")
    def test_get_movies_collection(self, get_database_mock):
        database_mock = MagicMock()
        collection_mock = MagicMock()

        def database_side_effect(key):
            return collection_mock if key == MONGODB_MOVIES_COLLECTION_NAME else None

        database_mock.__getitem__.side_effect = database_side_effect

        get_database_mock.return_value = database_mock

        returned_collection = get_movies_collection()

        get_database_mock.assert_called_once()

        assert returned_collection is collection_mock
