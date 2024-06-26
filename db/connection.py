import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection

load_dotenv()


def connect_db() -> connection:
    """
    Establishes a connection to the PostgreSQL database using credentials from environment variables.

    Environment Variables:
        DB_NAME (str): The name of the database.
        DB_USER (str): The database user.
        DB_PASSWORD (str): The password for the database user.
        DB_HOST (str): The host of the database.
        DB_PORT (str): The port of the database.

    Returns:
        connection: A connection object to the PostgreSQL database.
    """
    connect = psycopg2.connect(
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT')
    )
    return connect
