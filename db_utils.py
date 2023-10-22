"""Module with light database class wrapper"""
import polars as pl

class psqldb:
    """
    Database class with utility functions for interacting with the 
    postgreSQL database.
    """

    def __init__(self, dbname: str):
        self.dbname = dbname
        self.uri = f"postgresql://postgres:postgres@localhost:5432/{self.dbname}"

    def run_query(self, query: list[str] | str) -> pl.DataFrame:
        return pl.read_database(query=query, connection_uri=self.uri)

    def run_sql_file(self, path) -> pl.DataFrame:
        sqlfile = open(path, "r")
        return self.run_query(sqlfile.read())
