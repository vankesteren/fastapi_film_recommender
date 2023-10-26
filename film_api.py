"""API for the film rental recommender system."""

from fastapi import FastAPI

from recommender import (
    postgres_db,
    get_film_information,
    get_past_rentals,
    get_recommendations,
)

# init fastapi
app = FastAPI(
    title="Film recommendation API",
    summary="Recommend films based on past rentals",
    version="0.1.0",
    license_info={"name": "MIT", "url": "https://mit-license.org/"},
)


@app.get("/customers/{customer_id}")
def get_customer_by_id(customer_id: int) -> list[dict]:
    """# Get customer information.

    This endpoint queries the database and returns
    customer information.
    """
    return postgres_db.run_query(
        f"""
        select *
        from customer
        where customer_id={customer_id}
        """,
    ).to_dicts()


@app.get("/recommend/{customer_id}")
def recommend(customer_id: int, n: int = 5):
    """# Get recommendations.

    This endpoint queries the database for past
    rentals and then returns a recommendation
    """
    past_rentals = get_past_rentals(customer_id)
    recs = get_recommendations(past_rentals, n_rec=n)
    return get_film_information(recs)
