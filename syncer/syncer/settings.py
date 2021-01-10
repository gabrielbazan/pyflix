

MONGODB_HOST = "movies_db"
MONGODB_PORT = 27017
MONGODB_USERNAME = "movies_user"
MONGODB_PASSWORD = "movies_password"
MONGODB_DATABASE_NAME = "movies_db"
MONGODB_MOVIES_COLLECTION_NAME = "movies"

PROVIDER_URL = "https://ghibliapi.herokuapp.com"

PROVIDER_LIMIT_PARAMETER = "limit"

PROVIDER_FILMS_URL_PATH = "films"
PROVIDER_FILMS_LIMIT = 250
PROVIDER_FILMS_SUCCESS_CODE = 200

PROVIDER_PEOPLE_URL_PATH = "people"
PROVIDER_PEOPLE_LIMIT = 250
PROVIDER_PEOPLE_SUCCESS_CODE = 200

PROVIDER_SPECIES_URL_PATH = "species"
PROVIDER_SPECIES_LIMIT = 250
PROVIDER_SPECIES_SUCCESS_CODE = 200


class ProviderFilmField(object):
    ID = "id"
    TITLE = "title"


class ProviderPersonField(object):
    FILMS = "films"
    NAME = "name"
    SPECIE = "species"


class ProviderSpeciesField(object):
    ID = "id"
    NAME = "name"


PROVIDER_HUMAN_SPECIE_NAME = "Human"
SPECIES_TO_INGEST = [PROVIDER_HUMAN_SPECIE_NAME]


class MovieField(object):
    ID = "id"
    TITLE = "title"
    PEOPLE = "people"
    PERSON_NAME = "name"


IMPORT_INTERVAL = 15
