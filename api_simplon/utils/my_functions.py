import urllib.parse
from dotenv import load_dotenv
load_dotenv()
import os

def get_connection_uri():
    """
    Retrieves the connection URI for the database.
    Reads URI parameters from the environment or uses default values.
    If the database is SQLite, returns the SQLite connection URI.
    If the database is PostgreSQL, returns the PostgreSQL connection URI.
    Returns:
        str: The connection URI for the database.
    """
   
    # Read URI parameters from the environment or use default values
    dbhost = os.getenv('DBHOST', 'localhost')  # Default to 'localhost'
    dbname = os.getenv('DBNAME', 'mydatabase')  # Default database name
    dbuser = urllib.parse.quote(os.getenv('DBUSER', 'myuser'))  # Default user
    password = urllib.parse.quote(os.getenv('PASSWORD', 'mypassword'))  # Default password
    use_sqlie = os.getenv('DB_SQLITE', "False")  # Default to False

    # Check if the database is SQLite
    if use_sqlie == "True":
        # Return the SQLite connection URI
        db_uri = f"sqlite:///data/{dbname}.db"
    else:
        # Return the PostgreSQL connection URI
        db_uri = f"postgresql://{dbuser}:{password}@{dbhost}/{dbname}"
    
    return db_uri