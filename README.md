# PyFlix


PyFlix is a very simple movies catalog, that feeds from 
the [Ghibli API](https://ghibliapi.herokuapp.com/).


It has the following services:
 * A **MongoDB** containing movies metadata.
 * The metadata in MongoDB is refreshed in time intervals, by a component named **Syncer**.
 * The **WebApp** service, serves a list of all the movies in the database. It is a Flask app.


## Setting up the environment

It is yet another docker-compose app.

### Build

```
docker-compose build
```

### Start

```
docker-compose up
```


## Usage

The WebApp is served in the port _8000_ of the host machine.
* Go to http://0.0.0.0:8000 to see a hello message from the WebApp service.
* Go to http://0.0.0.0:8000/movies to see the movies list.
