from pathlib import Path
from db_utils import psqldb
import polars as pl

QPATH = Path("queries")
db = psqldb("pagila")

db.run_query("select * from customer")
db.run_query("select customer_id, rental_id, rental.inventory_id, inventory.film_id from rental left join inventory on rental.inventory_id=inventory.inventory_id")
db.run_sql_file(QPATH / "past_rentals.sql")