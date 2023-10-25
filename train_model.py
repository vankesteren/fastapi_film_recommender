
import warnings
import pickle
from db_utils import psqldb
import polars as pl
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt

# turn off warning for conversion without column names
warnings.filterwarnings(action='ignore', category=UserWarning)

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
tfidf_transformer = TfidfTransformer()
rental_matrix_tfidf = tfidf_transformer.fit_transform(rental_matrix[:,1:])

# Latent semantic analysis
model = TruncatedSVD(n_components=50)
model.fit(rental_matrix_tfidf)

# store model
with open("model/tfidf_transformer.pkl", "wb") as trf_file:
    pickle.dump(tfidf_transformer, file=trf_file)
with open("model/model.pkl", "wb") as mod_file:
    pickle.dump(model, file=mod_file)

# test model
def get_recommendation(articles_bought: list[int], n_rec=5):
    x = np.zeros(1000, int)
    for a in articles_bought:
        x[a - 1] += 1
    w = model.transform(transformer.transform([x]))
    xhat = model.inverse_transform(w)
    rank = xhat.argsort()[0].tolist()
    rank += 1
    recommendations: list[int] = []
    while len(recommendations) < n_rec:
        item = rank.pop()
        if not item in articles_bought:
            recommendations.append(item)

    return recommendations # last 5 items in reverse order


model.inverse_transform(model.transform(rental_matrix_tfidf))
model.explained_variance_ratio_.cumsum()

get_recommendation([1, 45, 323])
get_recommendation(np.where(rental_matrix[0,1:])[1]+1)