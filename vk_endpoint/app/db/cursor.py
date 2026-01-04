"""cursor håndtering så flere forbindelser til databasen kan ekistere på samme tid."""

from collections.abc import Generator

from db.connection import get_conn, put_conn
from fastapi import Depends
from psycopg2.extensions import connection, cursor


def get_db() -> Generator[connection, None, None]:
    """Starter og slutter forbindelse til database."""
    conn = get_conn()
    try:
        yield conn
    finally:
        put_conn(conn)


# Cursor dependency
def get_cursor(conn: connection = Depends(get_db)) -> Generator[cursor, None, None]:  # noqa: B008
    """Laver en cursor instance og automatisk lukker den ved slutningen requesten."""
    with conn.cursor() as cur:
        yield cur
