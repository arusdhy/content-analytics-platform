# Loads environment variables for database configuration
import os
from dotenv import load_dotenv

load_dotenv()

print("ENV FILE LOADED:", os.path.exists(".env"))

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}