from time import sleep
import logging
from settings import MovieField
from metadata_provider import MetadataProviderGateway
from serialization import MetadataSerializer
from database import get_movies_collection


LOGGER = logging.getLogger(__name__)


class Daemon(object):

    def __init__(self, interval):
        self.interval = interval

    def start(self):
        while True:
            self._run()
            sleep(self.interval)

    def _run(self):
        raise NotImplementedError()


class MetadataSyncerDaemon(Daemon):

    def _run(self):
        try:
            MetadataSyncer.synchronize_with_provider()
        except:
            LOGGER.exception("An error occurred while syncing")


class MetadataSyncer(object):

    @staticmethod
    def synchronize_with_provider():
        LOGGER.info("Synchronizing with metadata provider")

        metadata = MetadataSyncer.get_metadata_from_provider()
        serialized_movies = MetadataSyncer.serialize_metadata(metadata)
        MetadataSyncer.save_movies(serialized_movies)

        LOGGER.info("Done synchronizing with metadata provider")

    @staticmethod
    def get_metadata_from_provider():
        films = MetadataProviderGateway.get_films()
        people = MetadataProviderGateway.get_people()
        species = MetadataProviderGateway.get_species()
        return films, people, species

    @staticmethod
    def serialize_metadata(metadata):
        return MetadataSerializer(*metadata).serialize()

    @staticmethod
    def save_movies(movies):
        movies_collection = get_movies_collection()
        MetadataSyncer.save_movies_to_collection(movies, movies_collection)

    @staticmethod
    def save_movies_to_collection(movies, movies_collection):
        for movie in movies:
            MetadataSyncer.save_movie_to_collection(movies_collection, movie)

    @staticmethod
    def save_movie_to_collection(movies_collection, movie):
        filters = {MovieField.ID: movie.get(MovieField.ID)}
        updates = {"$set": movie}
        return movies_collection.find_one_and_update(filters, updates, upsert=True)
