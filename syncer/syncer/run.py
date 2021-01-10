import logging
from settings import IMPORT_INTERVAL
from syncer import MetadataSyncerDaemon


LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    daemon = MetadataSyncerDaemon(IMPORT_INTERVAL)

    LOGGER.info("Starting metadata syncer daemon")

    daemon.start()
