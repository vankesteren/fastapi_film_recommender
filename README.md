# Small proof-of-concept of API-based recommendation system

## Tech stack:
- 🐘 [PostgreSQL](https://www.postgresql.org/), with pagila database from [xzilla/pagila](https://github.com/xzilla/pagila); see also [the schema](https://zwbetz-gh.github.io/schemaspy-postgres-github-pages/tables/film.html)
- 🐻 [polars](https://www.pola.rs/) for running queries and local dataframe features
- 📈 [scikit-learn](https://scikit-learn.org/) for creating a simple product recommender
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) for turning this into a microservice
- 🐋 [Docker](https://www.docker.com/) for containerizing the whole application 

## Installation

1. Install postgresql
2. Clone this repo
3. run `git clone https://github.com/JannikArndt/PostgreSQLSampleDatabase.git`
4. run `create_database.bat` (or the `.sh` script from the original repo) to generate the database
5. `docker build . -t recommender`
6. `docker run recommender`
