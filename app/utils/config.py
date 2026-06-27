# Configuration file for database connection settings
import os
# Import function that loads variables from .env file into the environment
from dotenv import load_dotenv
# Load variables from .env file into environment variables
load_dotenv()
# Create a dictionary that stores database configuration
# Values are pulled from environment variables (not hardcoded for security)
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}