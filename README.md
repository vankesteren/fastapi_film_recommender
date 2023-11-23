# Film rental recommender

This repository implements a recommender system microservice on top of an example database of film rentals. The recommender is accessible as an API via the browser.

The recommender is a basic collaborative filtering method based on [latent semantic analysis](https://en.wikipedia.org/wiki/Latent_semantic_analysis) - a truncated singular value decomposition of a TFiDF transformed customer-rental matrix. 

> Note that the results are nonsensical because the data is just an example database, but the method should in principle work!

## Tech stack 🏗️
- 🐘 [PostgreSQL](https://www.postgresql.org/), with example database from [xzilla/pagila](https://github.com/xzilla/pagila); see also [the schema](https://zwbetz-gh.github.io/schemaspy-postgres-github-pages/tables/film.html)
- 🐻‍❄️ [polars](https://www.pola.rs/) for running queries and dataframe operations
- 📈 [scikit-learn](https://scikit-learn.org/) for creating a simple product recommender
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) for turning this into a microservice
- 🐋 [Docker](https://www.docker.com/) for containerizing the whole application 

## Installation 📦

1. Install docker
2. Clone this repository
3. Run `docker compose up`
4. Navigate to [localhost:8000/recommend/1?n=5](https://localhost:8000/recommend/1?n=5) or see the docs at [localhost:8000/docs](https://localhost:8000/docs)

For different installation methods and development, see [here](installation.md).

## Structure 

The repo is structured as follows:

![](img/recommender_diagram.svg)


## Why did I make this?

I wanted to try out FastAPI and Docker, and for me having a specific project is always the best motivation to learn new stuff -- even if it's just a toy project! 