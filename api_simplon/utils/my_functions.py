import urllib.parse
from dotenv import load_dotenv
load_dotenv()
import os

def get_connection_uri():
    # Read URI parameters from the environment or use default values
    dbhost = os.getenv('DBHOST', 'localhost')  # Default to 'localhost'
    dbname = os.getenv('DBNAME', 'mydatabase')  # Default database name
    dbuser = urllib.parse.quote(os.getenv('DBUSER', 'myuser'))  # Default user
    password = urllib.parse.quote(os.getenv('PASSWORD', 'mypassword'))  # Default password

    # Create the connection URI
    db_uri = f"postgresql://{dbuser}:{password}@{dbhost}/{dbname}"
    return db_uri