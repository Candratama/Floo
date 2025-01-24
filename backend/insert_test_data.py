"""
Script to insert test data directly into the database
"""
import json
import logging
from datetime import datetime
from sqlmodel import Session, select
from app.db.session import engine
from app.models.user import User
from app.models.bank import Bank
from app.models.category import Category
from app.models.transaction import Transaction
from app.core.security import get_password_hash

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_test_data():
    """Load test data from JSON file"""
    with open('tests/test_data.json') as f:
        return json.load(f)

def cleanup_existing_data(session: Session):
    """Remove existing test data"""
    try:
        # Delete in correct order due to foreign key constraints
        session.exec("DELETE FROM users")
        session.exec("DELETE FROM categories")
        session.exec("DELETE FROM banks")
        session.exec("DELETE FROM transactions")
        session.commit()
        logger.info("✅ Cleaned up existing data")
    except Exception as e:
        logger.error(f"❌ Error cleaning up data: {e}")
        raise

def insert_users(session: Session, user_data_list):
    """Insert test users"""
    users = {}
    try:
        for user_data in user_data_list:
            # Hash the password
            hashed_password = get_password_hash(user_data["password"])
            
            # Create user
            db_user = User(
                fullname=user_data["fullname"],
                username=user_data["username"],
                email=user_data["email"],
                password=hashed_password
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            
            # Store user mapping for later use
            users[user_data["username"]] = db_user
            logger.info(f"✅ Created user: {user_data['username']}")
            
        return users
    except Exception as e:
        logger.error(f"❌ Error creating users: {e}")
        raise

def insert_banks(session: Session, bank_data_list, users):
    """Insert test banks"""
    banks = {}
    try:
        for bank_data in bank_data_list:
            db_bank = Bank(
                name=bank_data["name"],
                color=bank_data["color"],
                start_balance=bank_data["start_balance"],
                end_balance=bank_data["start_balance"],
                user_id=bank_data["user_id"]
            )
            session.add(db_bank)
            session.commit()
            session.refresh(db_bank)
            
            banks[db_bank.id] = db_bank
            logger.info(f"✅ Created bank: {bank_data['name']}")
            
        return banks
    except Exception as e:
        logger.error(f"❌ Error creating banks: {e}")
        raise

def insert_categories(session: Session, category_data_list):
    """Insert test categories"""
    categories = {}
    try:
        # Combine expense and income categories
        for category_data in category_data_list:
            db_category = Category(
                name=category_data["name"],
                is_income=category_data["is_income"],
                user_id=category_data["user_id"]
            )
            session.add(db_category)
            session.commit()
            session.refresh(db_category)
            
            categories[db_category.id] = db_category
            logger.info(f"✅ Created category: {category_data['name']}")
            
        return categories
    except Exception as e:
        logger.error(f"❌ Error creating categories: {e}")
        raise

def insert_transactions(session: Session, transaction_data_list):
    """Insert test transactions"""
    try:
        for transaction_data in transaction_data_list:
            db_transaction = Transaction(
                date=datetime.strptime(transaction_data["date"], "%Y-%m-%d").date(),
                amount=transaction_data["amount"],
                description=transaction_data["description"],
                category_id=transaction_data["category_id"],
                bank_id=transaction_data["bank_id"],
                user_id=transaction_data["user_id"]
            )
            session.add(db_transaction)
            session.commit()
            session.refresh(db_transaction)
            
            logger.info(f"✅ Created transaction: {transaction_data['description']}")
            
    except Exception as e:
        logger.error(f"❌ Error creating transactions: {e}")
        raise

def main():
    """Main function to insert test data"""
    logger.info("Starting test data insertion...")
    
    try:
        # Load test data
        test_data = load_test_data()
        
        # Create database session
        with Session(engine) as session:
            # Cleanup existing data
            # cleanup_existing_data(session)
            
            # Insert users
            users = insert_users(session, test_data["user"]["register_multiple"])
            
            # Insert banks
            banks = insert_banks(session, test_data["bank"]["create_multiple"], users)
            
            # Insert all categories
            all_categories = test_data["category"]["create_multiple"]
            categories = insert_categories(session, all_categories)
            
            # Insert transactions
            insert_transactions(session, test_data["transaction"]["create_multiple"])
            
        logger.info("✨ Test data insertion completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error inserting test data: {e}")
        raise

if __name__ == "__main__":
    main()