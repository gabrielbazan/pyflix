from requests import get
from settings import (
    PROVIDER_URL,
    PROVIDER_LIMIT_PARAMETER,
    PROVIDER_FILMS_URL_PATH,
    PROVIDER_FILMS_LIMIT,
    PROVIDER_FILMS_SUCCESS_CODE,
    PROVIDER_PEOPLE_URL_PATH,
    PROVIDER_PEOPLE_LIMIT,
    PROVIDER_PEOPLE_SUCCESS_CODE,
    PROVIDER_SPECIES_URL_PATH,
    PROVIDER_SPECIES_LIMIT,
    PROVIDER_SPECIES_SUCCESS_CODE,
)
from utils import build_uri


class MetadataProviderError(Exception):
    pass


class MetadataProviderGateway(object):

    @staticmethod
    def get_films():
        return MetadataProviderGateway._get_all_from_collection(
            PROVIDER_FILMS_URL_PATH,
            PROVIDER_FILMS_SUCCESS_CODE,
            PROVIDER_FILMS_LIMIT,
        )

    @staticmethod
    def get_people():
        return MetadataProviderGateway._get_all_from_collection(
            PROVIDER_PEOPLE_URL_PATH,
            PROVIDER_PEOPLE_SUCCESS_CODE,
            PROVIDER_PEOPLE_LIMIT,
        )

    @staticmethod
    def get_species():
        return MetadataProviderGateway._get_all_from_collection(
            PROVIDER_SPECIES_URL_PATH,
            PROVIDER_SPECIES_SUCCESS_CODE,
            PROVIDER_SPECIES_LIMIT,
        )

    @staticmethod
    def _get_all_from_collection(url_path, success_code, limit):
        collection = Collection(url_path, success_code, limit)
        return collection.all()


class Collection(object):

    def __init__(self, path, success_code, limit):
        self.path = path
        self.success_code = success_code
        self.limit = limit

    def all(self):
        uri = build_uri(PROVIDER_URL, self.path)
        parameters = {PROVIDER_LIMIT_PARAMETER: self.limit}

        response = get(uri, params=parameters)

        status_code = response.status_code
        if status_code != self.success_code:
            raise MetadataProviderError(f"Got an unexpected status code: {status_code}")

        try:
            return response.json()
        except:
            raise MetadataProviderError(f"Could not parse response: '{response.text}'")
