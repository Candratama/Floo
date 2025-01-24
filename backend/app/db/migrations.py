"""
Database migrations for adding user_id to existing tables
"""
from sqlmodel import Session, text
from app.db.session import engine

def run_migrations():
    with Session(engine) as session:
        # Add user_id column to categories table
        session.exec(text("""
            ALTER TABLE categories 
            ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);
        """))
        
        # Add user_id column to banks table
        session.exec(text("""
            ALTER TABLE banks 
            ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);
        """))
        
        # Make user_id required after adding
        session.exec(text("""
            ALTER TABLE categories 
            ALTER COLUMN user_id SET NOT NULL;
        """))
        
        session.exec(text("""
            ALTER TABLE banks 
            ALTER COLUMN user_id SET NOT NULL;
        """))
        
        # Create indexes for better query performance
        session.exec(text("""
            CREATE INDEX IF NOT EXISTS idx_categories_user_id 
            ON categories(user_id);
        """))
        
        session.exec(text("""
            CREATE INDEX IF NOT EXISTS idx_banks_user_id 
            ON banks(user_id);
        """))
        
        session.exec(text("""
            CREATE INDEX IF NOT EXISTS idx_transactions_user_id 
            ON transactions(user_id);
        """))
        
        session.commit()

if __name__ == "__main__":
    run_migrations()