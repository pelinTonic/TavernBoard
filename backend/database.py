from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base 
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3


engine = create_engine("sqlite:///./tavern.db", connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

def get_db():

    """
    Provide a database session for dependency injection.

    This generator function creates a new SQLAlchemy database session
    and yields it for use in a request or operation. After the caller
    is done, the session is automatically closed to release resources.

    Yields:
        Session: An active SQLAlchemy database session.

    Ensures:
        The database session is properly closed after use, even if an
        exception occurs.
    """

    db = SessionLocal()  
    try:
        yield db          
    finally:
        db.close()       