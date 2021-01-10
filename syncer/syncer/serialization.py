import logging
from settings import (
    SPECIES_TO_INGEST,
    ProviderFilmField,
    ProviderPersonField,
    ProviderSpeciesField,
    MovieField,
)
from utils import URI_PATH_SEPARATOR


PROVIDER_TO_INTERNAL_FILM_FIELDS_MAP = {
    MovieField.ID: ProviderFilmField.ID,
    MovieField.TITLE: ProviderFilmField.TITLE,
}


PROVIDER_TO_INTERNAL_PERSON_FIELDS_MAP = {
    MovieField.PERSON_NAME: ProviderPersonField.NAME,
}


LOGGER = logging.getLogger(__name__)


class MetadataSerializer(object):

    def __init__(self, films, people, species):
        self.films = films
        self.people = people
        self.species = species

    def serialize(self):
        serialized_films = self.serialize_films()
        filtered_people = self.filter_people()
        MetadataSerializer.add_people_to_serialized_films(
            filtered_people, serialized_films
        )
        return serialized_films

    def serialize_films(self):
        return [
            MetadataSerializer.serialize_film(film)
            for film in self.films
        ]

    @staticmethod
    def serialize_film(film):
        return {
            internal_field: film.get(provider_field)
            for provider_field, internal_field in PROVIDER_TO_INTERNAL_FILM_FIELDS_MAP.items()
        }

    def filter_people(self):
        return [
            individual
            for individual in self.people
            if self.individual_is_importable(individual)
        ]

    def individual_is_importable(self, individual):
        species_identifiers = self.get_identifiers_of_species_to_import()
        species_identifier = MetadataSerializer.get_species_identifier_of_individual(
            individual
        )
        return species_identifier in species_identifiers

    def get_identifiers_of_species_to_import(self):
        return [
            MetadataSerializer.get_species_identifier(specie)
            for specie in self.species
            if MetadataSerializer.species_is_importable(specie)
        ]

    @staticmethod
    def species_is_importable(species):
        specie_name = species.get(ProviderSpeciesField.NAME)
        return specie_name in SPECIES_TO_INGEST

    @staticmethod
    def get_species_identifier(species):
        identifier = species.get(ProviderSpeciesField.ID)
        assert identifier, "Could not get identifier from species"
        return identifier

    @staticmethod
    def get_species_identifier_of_individual(individual):
        species_uri = individual.get(ProviderPersonField.SPECIE)
        return MetadataSerializer.get_identifier_from_resource_uri(
            species_uri
        )

    @staticmethod
    def add_people_to_serialized_films(people, serialized_films):
        serialized_films_map = MetadataSerializer.build_serialized_films_map(
            serialized_films
        )

        for individual in people:
            MetadataSerializer.add_individual_to_films(
                serialized_films_map, individual
            )

    @staticmethod
    def build_serialized_films_map(serialized_films):
        return {
            film.get(MovieField.ID): film
            for film in serialized_films
        }

    @staticmethod
    def add_individual_to_films(serialized_films_map, individual):
        individual_film_uris = individual.get(ProviderPersonField.FILMS, [])

        for film_uri in individual_film_uris:
            MetadataSerializer.add_individual_to_film(serialized_films_map, individual, film_uri)

    @staticmethod
    def add_individual_to_film(serialized_films_map, individual, film_uri):
        film = MetadataSerializer.get_film_from_map_or_none(serialized_films_map, film_uri)

        if film:
            MetadataSerializer.add_individual_to_film_object(individual, film)
        else:
            LOGGER.warning("Could not find '%s' film", film_uri)

    @staticmethod
    def get_film_from_map_or_none(serialized_films_map, film_uri):
        film_identifier = MetadataSerializer.get_identifier_from_resource_uri(
            film_uri
        )

        return serialized_films_map.get(film_identifier)

    @staticmethod
    def add_individual_to_film_object(individual, film):
        if MovieField.PEOPLE not in film:
            film[MovieField.PEOPLE] = []

        serialized_individual = MetadataSerializer.serialize_individual(individual)
        film[MovieField.PEOPLE].append(serialized_individual)

    @staticmethod
    def serialize_individual(individual):
        return {
            internal_field: individual.get(provider_field)
            for provider_field, internal_field in PROVIDER_TO_INTERNAL_PERSON_FIELDS_MAP.items()
        }

    @staticmethod
    def get_identifier_from_resource_uri(uri):
        components = uri.split(URI_PATH_SEPARATOR)
        return components[-1]
