"""Module with light database class wrapper."""
import polars as pl


class PSQLdb:
    """PostgreSQL database connector class.

    Light database class with utility functions for interacting with a
    postgreSQL database.
    """

    def __init__(
        self,
        dbname: str,
        user: str = "postgres",
        passwd: str = "postgres",
        host: str = "localhost",
        port: int = 5432,
    ):
        """Initialize the database connector."""
        self.dbname = dbname
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port

    @property
    def uri(self):
        """Return the current URI."""
        return f"postgresql://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.dbname}"

    def run_query(self, query: list[str] | str) -> pl.DataFrame:
        """Run query from string on the database."""
        return pl.read_database_uri(query=query, uri=self.uri)

    def run_sql_file(self, path: str) -> pl.DataFrame:
        """Run query on database from .sql file."""
        sqlfile = open(path)
        return self.run_query(sqlfile.read())
