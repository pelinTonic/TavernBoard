from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base 

engine = create_engine("sqlite:///./tavern.db", connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

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