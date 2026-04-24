from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth
from routers import campaign

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

app.add_middleware(CORSMiddleware, allow_origins = ["http://localhost:5173"], allow_credentials = True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(campaign.router)

