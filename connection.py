from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="kodeord",
    port="5432"
)

def get_conn():
    # Get a connection from the pool
    return connection_pool.getconn()

def put_conn(conn):
    # Return connection to the pool
    connection_pool.putconn(conn)