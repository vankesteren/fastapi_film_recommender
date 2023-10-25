import pickle
import numpy as np
from fastapi import FastAPI
from db_utils import psqldb

# Connect to database
postgres_db = psqldb("pagila")

# read model
with open("model/tfidf_transformer.pkl", "rb") as trf_file:
    tfidf_transformer = pickle.load(trf_file)
with open("model/model.pkl", "rb") as mod_file:
    model = pickle.load(mod_file)

def get_past_rentals(customer_id: int) -> list[int]:
    result = postgres_db.run_query(
        f"""
        select inventory.film_id 
        from rental 
        left join inventory 
        on rental.inventory_id=inventory.inventory_id
        where rental.customer_id={customer_id}
        """
    )
    return result[:,0].to_list()

def get_film_information(film_ids: list[int]) -> list[dict]:
    sql_ref = tuple(film_ids) if len(film_ids) > 1 else f"({film_ids[0]})"
    result = postgres_db.run_query(
        f"""
        select film_id, title, release_year as year, description, rating 
        from film 
        where film_id in {sql_ref}
        """
    )
    return result.to_dicts()


def get_recommendations(articles_bought: list[int], n_rec=5) -> list[int]:
    x = np.zeros(1000, int)
    for a in articles_bought:
        x[a - 1] += 1
    w = model.transform(tfidf_transformer.transform([x]))
    xhat = model.inverse_transform(w)
    rank = xhat.argsort()[0] + 1
    rank = rank.tolist()
    recs: list[int] = []
    while len(recs) < n_rec:
        item = rank.pop()
        if not item in articles_bought:
            recs.append(item)
    return recs

# init fastapi
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/customers/{customer_id}")
def get_customer_by_id(customer_id: int):
    return postgres_db.run_query(
        f"""
        select * 
        from customer 
        where customer_id={customer_id}
        """
    ).to_dicts()

@app.get("/recommend/{customer_id}")
def recommend(customer_id: int, n: int = 5):
    past_rentals = get_past_rentals(customer_id)
    recs = get_recommendations(past_rentals, n_rec=n)
    return get_film_information(recs)