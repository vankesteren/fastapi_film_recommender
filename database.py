"""Module with light database class wrapper."""
import os
from pathlib import Path

import polars as pl


class PSQLdb:
    """PostgreSQL database connector class.

    Light database class with utility functions for interacting with a
    PostgreSQL database.
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
    def uri(self) -> str:
        """Return the current URI."""
        return f"postgresql://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.dbname}"

    def run_query(self, query: list[str] | str) -> pl.DataFrame:
        """Run query from string on the database.

        NB: ensure that SQL query is sanitized before entering it
        into this function to prevent injection attacks.
        """
        return pl.read_database_uri(query=query, uri=self.uri)

    def run_sql_file(self, path: str) -> pl.DataFrame:
        """Run query on database from .sql file."""
        with Path(path).open("r") as sqlfile:
            return self.run_query(sqlfile.read())


class PagilaDB(PSQLdb):
    """Pagila database connection using environment variables."""

    def __init__(self):
        """Init the connection to the pagila database."""
        super().__init__(
            dbname=os.environ.get("DB_NAME", "pagila"),
            user=os.environ.get("DB_USER", "postgres"),
            passwd=os.environ.get("DB_PASSWD", "postgres"),
            host=os.environ.get("DB_HOSTNAME", "localhost"),
            port=os.environ.get("DB_PORT", 5432),
        )
