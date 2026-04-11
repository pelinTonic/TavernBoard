from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
from routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):

    """
    Manage the application lifespan events for the FastAPI app.

    This context manager is executed on application startup and shutdown.
    On startup, it initializes the database schema by creating all tables
    defined in the SQLAlchemy Base metadata. The application then runs
    while yielding control. Any teardown logic can be added after the yield
    if needed.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Control is yielded back to the FastAPI application runtime.
    """

    Base.metadata.create_all(bind=engine)
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)

