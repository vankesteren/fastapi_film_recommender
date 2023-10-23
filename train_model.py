from pathlib import Path
from db_utils import psqldb
import polars as pl
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import NMF, TruncatedSVD
import pickle
import matplotlib.pyplot as plt

# set up database connection and run basic query
db = psqldb("pagila")
rentals = db.run_sql_file("queries/rental_matrix.sql")

# left join with all possible combinations
full_df = \
    pl.DataFrame({
        "customer_id": [range(1, 601)],
        "film_id": [range(1, 1001)]
    }). \
    explode("customer_id"). \
    explode("film_id"). \
    with_columns(
        pl.col("customer_id").cast(pl.Int32),
        pl.col("film_id").cast(pl.Int32)
    ). \
    join(rentals, on=["customer_id", "film_id"], how="left"). \
    fill_null(0)

# pivot wider to create a count matrix
rental_matrix = full_df.pivot(
    values="n", 
    index="customer_id", 
    columns="film_id", 
    aggregate_function="sum"
)



# transform to tfidf matrix
transformer = TfidfTransformer()
rental_matrix_tfidf = transformer.fit_transform(rental_matrix[:,1:])

# estimate nonnegative matrix factorization model
model = TruncatedSVD(n_components=2)
model.fit(rental_matrix_tfidf)

W = model.transform(rental_matrix_tfidf)
H = model.components_

model.inverse_transform(W[1,:].reshape(1, -1)).argmax()

model.inverse_transform([[0,0]])

def get_recommendation(articles_bought: list[int]):
    x = np.zeros(1000, int)
    for a in articles_bought:
        x[a - 1] += 1
    model.inverse_transform(model.transform(transformer.transform([x]))).argsort() + 1

