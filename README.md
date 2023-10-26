# Small proof-of-concept of API-based recommendation system

## Tech stack:
- 🐘 [PostgreSQL](https://www.postgresql.org/), with pagila database from [xzilla/pagila](https://github.com/xzilla/pagila); see also [the schema](https://zwbetz-gh.github.io/schemaspy-postgres-github-pages/tables/film.html)
- 🐻 [polars](https://www.pola.rs/) for running queries and local dataframe features
- 📈 [scikit-learn](https://scikit-learn.org/) for creating a simple product recommender
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) for turning this into a microservice
- 🐋 [Docker](https://www.docker.com/) for containerizing the whole application 

## Installation & interactive use

1. Install PostgreSQL & python
2. Clone this repo and `cd` to it.
3. Install and generate the example database:
    ```sh
    git clone https://github.com/xzilla/pagila.git
    createdb -U postgres pagila
    psql -U postgres -d pagila -f pagila/pagila-schema.sql
    psql -U postgres -d pagila -f pagila/pagila-data.sql
    psql -U postgres -d pagila -c "CREATE extension tablefunc;"
    ```
4. Install python requirements:
    ```sh
    pip install -r requirements.txt
    ```
5. Run the recommender API via the `uvicorn` python package:
    ```sh
    uvicorn recommender:app
    ```
6. Navigate to [localhost:8000/recommender/1?n=5](https://localhost:8000/recommender/1?n=5). See the docs at [localhost:8000/docs](https://localhost:8000/docs)

## Docker

1. Build the docker container
    ```sh
    docker build . -t recommender
    ```
2. Run the docker container
    ```
    docker run recommender
    ```
