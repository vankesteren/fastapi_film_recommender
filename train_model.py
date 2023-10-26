
import warnings
import pickle
from database import psqldb
import polars as pl
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt

# turn off warning for conversion without column names
warnings.filterwarnings(action='ignore', category=UserWarning)

# set up database connection and run required queries
postgres_db = psqldb("pagila")
rentals = postgres_db.run_sql_file("queries/all_rentals.sql")
cids = postgres_db.run_query("select customer_id from customer")[:,0]
fids = postgres_db.run_query("select film_id from film")[:,0]

# left join with all possible combinations
full_df = \
    pl.DataFrame({
        "customer_id": [cids],
        "film_id": [fids]
    }). \
    explode("customer_id"). \
    explode("film_id"). \
    join(rentals, on=["customer_id", "film_id"], how="left"). \
    fill_null(0)


# pivot wider to create a count matrix
rental_matrix = full_df.pivot(
    values="n",
    index="customer_id",
    columns="film_id",
    aggregate_function="sum"
)

# remove customers that did not rent anything
rental_matrix = rental_matrix.filter(pl.sum(pl.exclude("customer_id")) > 0)

# transform to tfidf matrix
tfidf_transformer = TfidfTransformer()
rental_matrix_tfidf = tfidf_transformer.fit_transform(rental_matrix[:,1:])

# Latent semantic analysis
model = TruncatedSVD(n_components=20)
model.fit(rental_matrix_tfidf)

# store model
with open("model/tfidf_transformer.pkl", "wb") as trf_file:
    pickle.dump(tfidf_transformer, file=trf_file)
with open("model/model.pkl", "wb") as mod_file:
    pickle.dump(model, file=mod_file)
