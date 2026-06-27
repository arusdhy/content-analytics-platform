#connecting PostgreSQL database to python using psycopg2 library
import psycopg2
# Create a connection to the PostgreSQL database
# This connects Python → your local database server
conn = psycopg2.connect(
    dbname="content_db",
    user="postgres",
    password="password3",
    host="localhost",
    port="5432"
)
# Create a cursor object
# Cursor is used to run SQL commands
cur = conn.cursor()

# Execute a SQL query
cur.execute("SELECT version();")
print(cur.fetchone())

conn.close()
