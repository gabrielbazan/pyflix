from flask import Flask, render_template
from settings import (
    COMPONENT_NAME,
    STRICT_SLASHES,
    MOVIES_ENDPOINT,
    MOVIES_TEMPLATE_FILENAME,
    MOVIES_TEMPLATE_SERVICE_PARAMETER_NAME,
    MOVIES_TEMPLATE_MOVIES_PARAMETER_NAME,
)
from database import get_movies_collection


app = Flask(__name__)


app.url_map.strict_slashes = STRICT_SLASHES


@app.route("/")
def root():
    return f"Welcome to {COMPONENT_NAME}!"


@app.route(MOVIES_ENDPOINT)
def list_movies():
    collection = get_movies_collection()
    movies = collection.find()

    parameters = {
        MOVIES_TEMPLATE_SERVICE_PARAMETER_NAME: COMPONENT_NAME,
        MOVIES_TEMPLATE_MOVIES_PARAMETER_NAME: movies
    }

    return render_template(MOVIES_TEMPLATE_FILENAME, **parameters)
