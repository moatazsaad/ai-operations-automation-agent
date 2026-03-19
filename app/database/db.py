import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# creates and returns a database connection
def get_connection():
    # ensure DATABASE_URL exists
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables")

    # create a connection to the PostgreSQL database 
    conn = psycopg2.connect(DATABASE_URL)
    
    return conn