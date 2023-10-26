# Small API-based recommendation system

This repository implements a recommender system microservice on top of an example database. The recommender is accessible as an API via the browser.

## Tech stack:
- 🐘 [PostgreSQL](https://www.postgresql.org/), with pagila database from [xzilla/pagila](https://github.com/xzilla/pagila); see also [the schema](https://zwbetz-gh.github.io/schemaspy-postgres-github-pages/tables/film.html)
- 🐻 [polars](https://www.pola.rs/) for running queries and local dataframe features
- 📈 [scikit-learn](https://scikit-learn.org/) for creating a simple product recommender
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) for turning this into a microservice
- 🐋 [Docker](https://www.docker.com/) for containerizing the whole application 

# Installation
There are three different installation methods with various levels of containerization: 
- Fully local, not using docker at all
- Containerized database, local python
- Fully containerized API and database

## Fully local installation
1. Install PostgreSQL & python
2. Clone this repo and `cd` to it.
3. Install and generate the example database
    ```sh
    git clone https://github.com/xzilla/pagila.git
    mv pagila/pagila-schema.sql pagila/1_schema.sql
    mv pagila/pagila-data.sql pagila/2_data.sql
    rm pagila/pagila-insert-data.sql pagila/README
    createdb -U postgres pagila
    psql -U postgres -d pagila -f pagila/1_schema.sql
    psql -U postgres -d pagila -f pagila/2_data.sql
    psql -U postgres -d pagila -c "CREATE extension tablefunc;"
    ```
4. Install python requirements:
    ```sh
    pip install -r requirements.txt
    ```
5. Run the recommender API via the `uvicorn` python package:
    ```sh
    uvicorn film_recommender:app
    ```
6. Navigate to [localhost:8000/recommender/1?n=5](https://localhost:8000/recommender/1?n=5). See the docs at [localhost:8000/docs](https://localhost:8000/docs)

## Dockerized database

1. Install Python
2. Clone this repo and `cd` to it
3. Build and run the database dockerfile
    ```sh
    docker build . -f pagiladb.dockerfile -t pagiladb
    docker run -p 5432:5432 -e POSTGRES_DB=pagila -e POSTGRES_PASSWORD=postgres pagiladb
    ```
4. Install python requirements:
    ```sh
    pip install -r requirements.txt
    ```
5. Run the recommender API via the `uvicorn` python package:
    ```sh
    uvicorn film_recommender:app
    ```
6. Navigate to [localhost:8000/recommender/1?n=5](https://localhost:8000/recommender/1?n=5). See the docs at [localhost:8000/docs](https://localhost:8000/docs)

## Fully containerized API and database
1. First, build the containers and create a network
    ```sh
    docker build . -f pagiladb.dockerfile -t pagiladb
    docker build . -f filmapi.dockerfile -t filmapi
    docker network create film-rec
    ```
2. Then, run the docker containers in this network, exposing the API.
    ```sh
    docker run --name pagila_database -e POSTGRES_DB=pagila -e POSTGRES_PASSWORD=postgres --network film-rec pagiladb
    docker run --name film_recommender -e DB_HOSTNAME=pagila_database -p 8000:8000 --network film-rec filmapi
    ```
3. Navigate to [localhost:8000/recommender/1?n=5](https://localhost:8000/recommender/1?n=5). See the docs at [localhost:8000/docs](https://localhost:8000/docs)