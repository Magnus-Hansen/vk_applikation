from db.connection import get_conn, put_conn
from fastapi import Depends


# Connection dependency
def get_db():
    conn = get_conn()
    try:
        yield conn
    finally:
        put_conn(conn)


# Cursor dependency
def get_cursor(conn=Depends(get_db)):
    with conn.cursor() as cur:
        yield cur
        # Cursor closes automatically at the end of request
