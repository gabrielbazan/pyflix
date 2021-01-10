import logging
from settings import HOST, PORT
from app import app


LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    LOGGER.info("Starting service")

    app.run(host=HOST, port=PORT)
