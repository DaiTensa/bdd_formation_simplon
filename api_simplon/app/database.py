from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils import my_functions

# Get the connection URI
DATABASE_URL = my_functions.get_connection_uri()

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class
Base = declarative_base()

def get_db():
    """
    Returns a database session.

    Returns:
        SessionLocal: The database session.

    Yields:
        SessionLocal: The database session.

    Raises:
        None

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()