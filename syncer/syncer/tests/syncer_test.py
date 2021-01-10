from unittest import TestCase
from unittest.mock import patch, MagicMock, call
from syncer import Daemon, MetadataSyncerDaemon, MetadataSyncer


MODULE = "syncer"


class DaemonTestCase(TestCase):

    def test_constructor(self):
        interval = MagicMock()
        daemon = Daemon(interval)
        assert daemon.interval is interval

    @patch(f"{MODULE}.sleep")
    def test_start(self, sleep_mock):
        daemon = Daemon(MagicMock())

        with self.assertRaises(NotImplementedError):
            daemon.start()

        sleep_mock.assert_not_called()

    @patch(f"{MODULE}.sleep")
    def test_start_sleep(self, sleep_mock):
        interval = MagicMock()
        daemon = Daemon(interval)
        daemon._run = MagicMock()

        sleep_mock.side_effect = InterruptedError

        with self.assertRaises(InterruptedError):
            daemon.start()

        sleep_mock.assert_called_once_with(interval)


class MetadataSyncerDaemonTestCase(TestCase):

    @patch(f"{MODULE}.MetadataSyncer")
    def test_run(self, metadata_syncer_mock):
        interval = MagicMock()
        metadata_syncer_daemon = MetadataSyncerDaemon(interval)

        metadata_syncer_daemon._run()

        metadata_syncer_mock.synchronize_with_provider.assert_called_once()


class MetadataSyncerTestCase(TestCase):

    @patch(f"{MODULE}.MetadataSyncer.save_movies")
    @patch(f"{MODULE}.MetadataSyncer.serialize_metadata")
    @patch(f"{MODULE}.MetadataSyncer.get_metadata_from_provider")
    def test_synchronize_with_provider(
        self,
        get_metadata_from_provider_mock,
        serialize_metadata_mock,
        save_movies_mock,
    ):
        metadata_mock = MagicMock()
        get_metadata_from_provider_mock.return_value = metadata_mock

        serialized_movies_mock = MagicMock()
        serialize_metadata_mock.return_value = serialized_movies_mock

        MetadataSyncer.synchronize_with_provider()

        get_metadata_from_provider_mock.assert_called_once()
        serialize_metadata_mock.assert_called_once_with(metadata_mock)
        save_movies_mock.assert_called_once_with(serialized_movies_mock)

    @patch(f"{MODULE}.MetadataProviderGateway")
    def test_get_metadata_from_provider(self, metadata_provider_gateway):
        films_mock = MagicMock()
        metadata_provider_gateway.get_films.return_value = films_mock

        people_mock = MagicMock()
        metadata_provider_gateway.get_people.return_value = people_mock

        species_mock = MagicMock()
        metadata_provider_gateway.get_species.return_value = species_mock

        returned_metadata = MetadataSyncer.get_metadata_from_provider()

        metadata_provider_gateway.get_films.assert_called_once()
        metadata_provider_gateway.get_people.assert_called_once()
        metadata_provider_gateway.get_species.assert_called_once()

        expected_metadata = (films_mock, people_mock, species_mock)

        self.assertEqual(returned_metadata, expected_metadata)

    @patch(f"{MODULE}.MetadataSerializer")
    def test_serialize_metadata(self, MetadataSerializer):
        metadata_mock = MagicMock(),

        metadata_serializer_instance_mock = MagicMock()
        MetadataSerializer.return_value = metadata_serializer_instance_mock

        MetadataSyncer.serialize_metadata(metadata_mock)

        MetadataSerializer.assert_called_once_with(*metadata_mock)
        metadata_serializer_instance_mock.serialize.assert_called_once()

    @patch(f"{MODULE}.get_movies_collection")
    @patch(f"{MODULE}.MetadataSyncer.save_movies_to_collection")
    def test_save_movies(self, save_movies_to_collection_mock, get_movies_collection_mock):
        movies_collection_mock = MagicMock()
        get_movies_collection_mock.return_value = movies_collection_mock

        movies_mock = MagicMock()
        MetadataSyncer.save_movies(movies_mock)

        get_movies_collection_mock.assert_called_once()

        save_movies_to_collection_mock.assert_called_once_with(
            movies_mock, movies_collection_mock
        )

    def test_save_movies_to_collection(self):
        MetadataSyncer.save_movie_to_collection = MagicMock()

        movies_mock = MagicMock(), MagicMock()
        movies_collection_mock = MagicMock()

        MetadataSyncer.save_movies_to_collection(movies_mock, movies_collection_mock)

        MetadataSyncer.save_movie_to_collection.assert_has_calls(
            [
                call(movies_collection_mock, movie_mock)
                for movie_mock in movies_mock
            ]
        )

    def test_save_movie_to_collection(self):
        movies_collection_mock = MagicMock()
        movie_mock = MagicMock()

        MetadataSyncer.save_movie_to_collection(movies_collection_mock, movie_mock)

        movies_collection_mock.find_one_and_update.assert_called_once()
