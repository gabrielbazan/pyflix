from unittest import TestCase
from unittest.mock import patch, MagicMock
from settings import (
    MOVIES_TEMPLATE_FILENAME,
    MOVIES_TEMPLATE_SERVICE_PARAMETER_NAME,
    MOVIES_TEMPLATE_MOVIES_PARAMETER_NAME,
)
from app import list_movies, COMPONENT_NAME


MODULE = "app"


class AppTestCase(TestCase):

    @patch(f"{MODULE}.render_template")
    @patch(f"{MODULE}.get_movies_collection")
    def test_list_movies(self, get_movies_collection_mock, render_template_mock):
        movies_collection_mock = MagicMock()
        get_movies_collection_mock.return_value = movies_collection_mock

        movies_mock = MagicMock()
        movies_collection_mock.find.return_value = movies_mock

        list_movies()

        get_movies_collection_mock.assert_called_once()
        movies_collection_mock.find.assert_called_once()

        mock_parameters = {
            MOVIES_TEMPLATE_SERVICE_PARAMETER_NAME: COMPONENT_NAME,
            MOVIES_TEMPLATE_MOVIES_PARAMETER_NAME: movies_mock
        }

        render_template_mock.assert_called_once_with(
            MOVIES_TEMPLATE_FILENAME, **mock_parameters
        )
