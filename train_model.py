"""Training latent semantic analysis model."""
import pickle
import warnings
from pathlib import Path

import polars as pl
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer

from database import PagilaDB

# turn off warning for conversion without column names
warnings.filterwarnings(action="ignore", category=UserWarning)

# set up database connection and run required queries
postgres_db = PagilaDB()
rentals = postgres_db.run_sql_file("queries/all_rentals.sql")
cids = postgres_db.run_query("select customer_id from customer")[:, 0]
fids = postgres_db.run_query("select film_id from film")[:, 0]

# left join with all possible combinations
full_df = (
    pl.DataFrame(
        {
            "customer_id": [cids],
            "film_id": [fids],
        }
    )
    .explode("customer_id")
    .explode("film_id")
    .join(rentals, on=["customer_id", "film_id"], how="left")
    .fill_null(0)
)


# pivot wider to create a count matrix
rental_matrix = full_df.pivot(
    values="n",
    index="customer_id",
    columns="film_id",
    aggregate_function="sum",
)

# remove customers that did not rent anything
rental_matrix = rental_matrix.filter(
    pl.sum_horizontal(pl.exclude("customer_id")) > 0
)

# transform to tfidf matrix
tfidf_transformer = TfidfTransformer()
rental_matrix_tfidf = tfidf_transformer.fit_transform(rental_matrix[:, 1:])

# Latent semantic analysis
model = TruncatedSVD(n_components=20)
model.fit(rental_matrix_tfidf)

# store model
with Path("model/tfidf_transformer.pkl").open("wb") as trf_file:
    pickle.dump(tfidf_transformer, file=trf_file)
with Path("model/model.pkl").open("wb")  as mod_file:
    pickle.dump(model, file=mod_file)
