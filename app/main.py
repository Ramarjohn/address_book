from fastapi import FastAPI

from app.core.logging import configure_logging, get_logger
from app.db.base import Base
from app.db.session import engine
from app.api.routes import router

configure_logging()
log = get_logger(__name__)

app = FastAPI(title="Address Book API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    # Create tables
    Base.metadata.create_all(bind=engine)
    log.info("Startup complete: tables ensured")

app.include_router(router)
