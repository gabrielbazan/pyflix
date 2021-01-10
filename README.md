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


## Notes to the reviewer

**Why using a database?** 
 Instead of having each process/thread its own copy of the data, it is better to have 
    a centralized place to store and manage the data. 
 * Better separation of concerns. 
 * Better scaling capabilities.
   * It does not matter how many threads are serving the data, we always sync 
     the data once (per time period). This means we're not killing the metadata provider API 
     with inefficient/duplicated calls.
   * The database has its own scaling capabilities. As most of the traffic is about reading,
        we'd have replicas.

**Why MongoDB?** 
 * It is a non-relational DB, meaning that the data schema is flexible, which
    is very useful when we're at early stages of our project.
 * It is also very quick to set up and use from Python.
 * Good scaling capabilities.
 * Widely used, and big community.

We would have used other options, like some RDBMS, other non-relational DB, or even Redis 
(with its limitations).

**Why having that "Syncer" service?** We have a better separation of concerns, and it's faster.

If there were no "syncer" service, the Flask threads would be responsible for: Serving 
the webpage, checking the age of the cached data, update the data when it is too 
old. If a thread has to update the data, it will take a long time to refresh it, and then 
respond. So time to time, we'll have a call to the webapp that is really slow. And what if
two calls are made to the webapp almost at the same time? There's no lock saying that some
other thread is updating the data, so the data would be updated twice at the same time.


**What did you unit test?** I tested the webapp route that serves the movies, and some of 
the most important classes in the Syncer service. I haven't done TDD, nor tested everything.
