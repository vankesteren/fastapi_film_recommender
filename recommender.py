from fastapi import FastAPI
from pathlib import Path
from db_utils import psqldb

# global settings
QPATH = Path("queries")
DB = psqldb("pagila")

# init fastapi
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/customers/{customer_id}")
def get_customer_by_id(customer_id: int):
    return DB. \
        run_query(f"select * from customer where customer_id={customer_id}"). \
        to_dicts()


# res = db.run_sql_file(QPATH / "alltables.sql")
# res.filter(pl.col("schemaname") == "webshop").select(pl.col("tablename")).to_numpy()
