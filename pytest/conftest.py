import psycopg2
import pytest


@pytest.fixture
def conn():
    conn = psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="Trixie",
        host="localhost",
        port=5432,
    )
    conn.autocommit = False

    # Prevent commit from ending the transaction
    with conn.cursor() as cur:
        cur.execute("BEGIN;")

    yield conn

    conn.rollback()
    conn.close()


@pytest.fixture(autouse=True)
def clean_db(conn):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE upload RESTART IDENTITY CASCADE;")
