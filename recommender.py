"""Functions to use a pre-trained latent semantic analysis model as a recommender."""
import os
import pickle
import warnings

import numpy as np

from database import PSQLdb

# turn off warning for sklearn transform conversion without column names
warnings.filterwarnings(action="ignore", category=UserWarning)

# Connect to database
postgres_db = PSQLdb(dbname="pagila", host=os.environ.get("DB_HOSTNAME", "localhost"))

# read model
with open("model/tfidf_transformer.pkl", "rb") as trf_file:
    tfidf_transformer = pickle.load(trf_file)
with open("model/model.pkl", "rb") as mod_file:
    model = pickle.load(mod_file)


# define functions required for recommender
def get_past_rentals(customer_id: int) -> list[int]:
    """Get past rentals for a specific customer.

    Args:
    ----
        customer_id: integer value of the requested customer.

    Returns:
    -------
        A list of integer film ids. If customer id
        does not exist, an empty list.
    """
    result = postgres_db.run_query(
        f"""
        select inventory.film_id
        from rental
        left join inventory
        on rental.inventory_id=inventory.inventory_id
        where rental.customer_id={customer_id}
        """,
    )
    return result[:, 0].to_list()


def get_film_information(film_ids: list[int]) -> list[dict]:
    """Get film information for a list of film ids.

    Args:
    ----
        film_ids: list of integers of film ids.

    Returns:
    -------
        film_id, title, year, description and rating for the films.
    """
    sql_ref = tuple(film_ids) if len(film_ids) > 1 else f"({film_ids[0]})"
    result = postgres_db.run_query(
        f"""
        select film_id, title, release_year as year, description, rating
        from film
        where film_id in {sql_ref}
        """,
    )
    return result.to_dicts()


def get_recommendations(rented_films: list[int], n_rec=5) -> list[int]:
    """Get recommendations based on rented films.

    Using a pre-trained latent semantic analysis model.

    Args:
    ----
        rented_films: list of integers of film_id
        n_rec: number of recommendations desired

    Returns:
    -------
        list of recommended film_ids
    """
    x = np.zeros(1000, int)
    for a in rented_films:
        x[a - 1] += 1
    w = model.transform(tfidf_transformer.transform([x]))
    xhat = model.inverse_transform(w)
    rank = xhat.argsort()[0] + 1
    rank = rank.tolist()
    recs: list[int] = []
    while len(recs) < n_rec:
        item = rank.pop()
        if item not in rented_films:
            recs.append(item)
    return recs
