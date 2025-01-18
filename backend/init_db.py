# backend/init_db.py
import logging
from sqlmodel import SQLModel
from app.db.session import engine
from app.models.user import User
from app.models.bank import Bank
from app.models.category import Category
from app.models.transaction import Transaction
from app.core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    logger.info("Creating database tables...")
    try:
        SQLModel.metadata.drop_all(engine)
        logger.info("Dropped all existing tables")
        
        SQLModel.metadata.create_all(engine)
        logger.info("Successfully created all tables")
        
        logger.info("""
Tables created:
- users
- banks
- categories
- transactions
        """)
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise e

def main():
    logger.info("Starting database initialization...")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    init_database()
    logger.info("Database initialization completed!")

if __name__ == "__main__":
    main()