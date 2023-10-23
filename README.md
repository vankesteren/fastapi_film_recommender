# Small proof-of-concept of API-based recommendation system

## Tech stack:
- 🐘 [PostgreSQL](https://www.postgresql.org/), with pagila database from [xzilla/pagila](https://github.com/xzilla/pagila); see also [the schema](https://zwbetz-gh.github.io/schemaspy-postgres-github-pages/tables/film.html)
- 🐻 [polars](https://www.pola.rs/) for running queries and local dataframe features
- 📈 [scikit-learn](https://scikit-learn.org/) for creating a simple product recommender
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) for turning this into a microservice
- 🐋 [Docker](https://www.docker.com/) for containerizing the whole application 

## Installation

1. Install PostgreSQL & Docker
2. Clone this repo and `cd` to it.
3. Install and generate the example database:
    ```sh
    git clone https://github.com/xzilla/pagila.git
    createdb -U postgres pagila
    psql -U postgres -d pagila -f pagila/pagila-schema.sql
    psql -U postgres -d pagila -f pagila/pagila-data.sql
    psql -U postgres -d pagila -c "CREATE extension tablefunc;"
    ```
4. Build the docker container
    ```sh
    docker build . -t recommender
    ```
5. Run the docker container
    ```
    docker run recommender
    ```
