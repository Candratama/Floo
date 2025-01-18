# app/db/session.py
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # Untuk melihat SQL queries
)

def init_db():
    try:
        SQLModel.metadata.drop_all(engine)  # Hapus semua tabel yang ada
        SQLModel.metadata.create_all(engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise e

def get_session():
    with Session(engine) as session:
        yield session