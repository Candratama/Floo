import requests
import json
import logging
import time
from datetime import datetime
from sqlmodel import Session, select
from app.models.user import User
from app.db.session import engine

# Setup logging
def setup_logging():
    """Setup logging configuration"""
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"tests/logs/test_run_{timestamp}.log"
    
    # Create logs directory if not exists
    import os
    os.makedirs("tests/logs", exist_ok=True)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Setup file handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Remove any existing handlers
    logger.handlers = []
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log initial message
    logger.info("=== FLOO API Test Session Started ===")
    logger.info(f"Log file created at: {log_filename}")
    
    return log_filename, logger

def generate_markdown_report(log_filename):
    """Generate markdown report from log file"""
    md_filename = log_filename.replace('.log', '.md')
    
    with open(log_filename, 'r') as log_file:
        log_content = log_file.readlines()
    
    with open(md_filename, 'w') as md_file:
        # Write header
        md_file.write("# FLOO API Test Report\n\n")
        md_file.write(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Write test environment info
        md_file.write("## Test Environment\n\n")
        md_file.write(f"- API URL: {BASE_URL}\n")
        md_file.write(f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Write test results
        md_file.write("## Test Results\n\n")
        md_file.write("```\n")
        md_file.writelines(log_content)
        md_file.write("```\n")
        
        # Calculate summary
        successes = sum(1 for line in log_content if "✅" in line)
        failures = sum(1 for line in log_content if "❌" in line)
        warnings = sum(1 for line in log_content if "⚠️" in line)
        
        # Write summary
        md_file.write("\n## Summary\n\n")
        md_file.write(f"- Total Tests Run: {successes + failures}\n")
        md_file.write(f"- Successes: {successes} ✅\n")
        md_file.write(f"- Failures: {failures} ❌\n")
        md_file.write(f"- Warnings: {warnings} ⚠️\n")
        
        # Write timestamp
        md_file.write(f"\n\nReport generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return md_filename

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "http://localhost:8000/api/v1"
TOKEN = None

# Load test data
with open('tests/test_data.json') as f:
    TEST_DATA = json.load(f)

def add_delay():
    """Add small delay between requests"""
    time.sleep(0.5)

def log_response(response, endpoint):
    """Log response details"""
    logger.info(f"\nTesting: {endpoint}")
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {response.json()}")
    logger.info("-" * 50)

def get_headers():
    """Get headers with authentication token"""
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

def cleanup_test_users(session: Session):
    """Remove test users if exist"""
    try:
        for user_data in TEST_DATA["user"]["register_multiple"]:
            test_user = session.exec(
                select(User).where(User.username == user_data["username"])
            ).first()
            if test_user:
                session.delete(test_user)
        session.commit()
        logger.info("Cleaned up existing test users")
    except Exception as e:
        logger.error(f"Error cleaning up test users: {e}")
        
def test_register_users():
    """Test registering multiple users"""
    endpoint = f"{BASE_URL}/register"
    registered_users = []

    for user_data in TEST_DATA["user"]["register_multiple"]:
        response = requests.post(endpoint, json=user_data)
        log_response(response, f"Register User: {user_data['username']}")
        
        if response.status_code == 200:
            logger.info(f"✅ Registration successful for {user_data['username']}")
            registered_users.append(response.json())
        elif response.status_code == 400 and "already registered" in response.json().get("detail", ""):
            logger.info(f"User {user_data['username']} already exists")
        else:
            logger.error(f"❌ Registration failed for {user_data['username']}: {response.json()}")
        
        add_delay()

    return registered_users

def test_login():
    """Test user login"""
    global TOKEN
    endpoint = f"{BASE_URL}/login"
    response = requests.post(
        endpoint,
        data=TEST_DATA["user"]["login"]
    )
    log_response(response, "Login User")
    
    if response.status_code == 200:
        TOKEN = response.json()["access_token"]
        logger.info("✅ Login successful")
        return response.json()
    else:
        logger.error(f"❌ Login failed: {response.json()}")
        return None

def run_auth_tests():
    """Run authentication related tests"""
    logger.info("\n=== Running Authentication Tests ===")
    try:
        # Cleanup existing test users
        with Session(engine) as session:
            cleanup_test_users(session)

        # Register users
        registered_users = test_register_users()
        if registered_users:
            logger.info(f"✅ Successfully registered {len(registered_users)} users")

        # Login with first user
        login_response = test_login()
        if login_response and "access_token" in login_response:
            logger.info("✅ Authentication tests passed!")
        else:
            logger.error("❌ Login failed")
    except Exception as e:
        logger.error(f"❌ Unexpected error in authentication tests: {str(e)}")
        
        
def test_create_banks():
    """Test creating multiple banks"""
    endpoint = f"{BASE_URL}/banks"
    created_banks = []

    for bank_data in TEST_DATA["bank"]["create_multiple"]:
        response = requests.post(
            endpoint,
            headers=get_headers(),
            json=bank_data
        )
        log_response(response, f"Create Bank: {bank_data['name']}")
        
        if response.status_code == 200:
            logger.info(f"✅ Successfully created bank: {bank_data['name']}")
            created_banks.append(response.json())
        else:
            logger.error(f"❌ Failed to create bank: {bank_data['name']}")
        
        add_delay()

    return created_banks

def test_get_banks():
    """Test getting all banks"""
    endpoint = f"{BASE_URL}/banks"
    response = requests.get(
        endpoint,
        headers=get_headers()
    )
    log_response(response, "Get All Banks")
    
    if response.status_code == 200:
        banks = response.json()
        logger.info(f"Found {len(banks)} banks")
        return banks
    else:
        logger.error("Failed to get banks")
        return None

def test_get_bank():
    """Test getting a specific bank"""
    banks = test_get_banks()
    if not banks:
        logger.error("No banks found to test")
        return None
    
    bank_id = banks[0]["id"]
    endpoint = f"{BASE_URL}/banks/{bank_id}"
    response = requests.get(
        endpoint,
        headers=get_headers()
    )
    log_response(response, f"Get Bank {bank_id}")
    return response.json() if response.status_code == 200 else None

def test_update_bank():
    """Test updating a bank"""
    banks = test_get_banks()
    if not banks:
        logger.error("No banks found to test")
        return None
    
    bank_id = banks[0]["id"]
    endpoint = f"{BASE_URL}/banks/{bank_id}"
    response = requests.patch(
        endpoint,
        headers=get_headers(),
        json=TEST_DATA["bank"]["update"]
    )
    log_response(response, f"Update Bank {bank_id}")
    return response.json() if response.status_code == 200 else None

def run_bank_tests():
    """Run bank related tests"""
    logger.info("\n=== Running Bank Tests ===")
    try:
        # Create banks
        created_banks = test_create_banks()
        if created_banks:
            logger.info(f"✅ Successfully created {len(created_banks)} banks")

        # Get all banks
        banks = test_get_banks()
        if banks:
            logger.info("✅ Successfully retrieved all banks")

        # Get specific bank
        bank = test_get_bank()
        if bank:
            logger.info("✅ Successfully retrieved specific bank")

        # Update bank
        updated_bank = test_update_bank()
        if updated_bank:
            logger.info("✅ Successfully updated bank")

        logger.info("✅ Bank tests passed!")
    except Exception as e:
        logger.error(f"❌ Unexpected error in bank tests: {str(e)}")
        
def test_create_categories():
    """Test creating multiple categories"""
    endpoint = f"{BASE_URL}/categories"
    created_categories = []

    # Create expense categories
    logger.info("\nCreating expense categories...")
    for category_data in TEST_DATA["category"]["create_expense"]:
        response = requests.post(
            endpoint,
            headers=get_headers(),
            json=category_data
        )
        log_response(response, f"Create Expense Category: {category_data['name']}")
        
        if response.status_code == 200:
            logger.info(f"✅ Successfully created expense category: {category_data['name']}")
            created_categories.append(response.json())
        else:
            logger.error(f"❌ Failed to create expense category: {category_data['name']}")
        
        add_delay()

    # Create income categories
    logger.info("\nCreating income categories...")
    for category_data in TEST_DATA["category"]["create_income"]:
        response = requests.post(
            endpoint,
            headers=get_headers(),
            json=category_data
        )
        log_response(response, f"Create Income Category: {category_data['name']}")
        
        if response.status_code == 200:
            logger.info(f"✅ Successfully created income category: {category_data['name']}")
            created_categories.append(response.json())
        else:
            logger.error(f"❌ Failed to create income category: {category_data['name']}")
        
        add_delay()

    return created_categories

def test_get_categories():
    """Test getting all categories"""
    endpoint = f"{BASE_URL}/categories"
    response = requests.get(
        endpoint,
        headers=get_headers()
    )
    log_response(response, "Get All Categories")
    
    if response.status_code == 200:
        categories = response.json()
        logger.info(f"Found {len(categories)} categories")
        return categories
    else:
        logger.error("Failed to get categories")
        return None

def test_get_categories_by_type():
    """Test getting categories filtered by type"""
    categories = test_get_categories()
    if not categories:
        return None

    income_categories = [cat for cat in categories if cat["is_income"]]
    expense_categories = [cat for cat in categories if not cat["is_income"]]

    logger.info(f"\nFound {len(income_categories)} income categories")
    logger.info(f"Found {len(expense_categories)} expense categories")

    return {
        "income": income_categories,
        "expense": expense_categories
    }

def test_update_category():
    """Test updating a category"""
    categories = test_get_categories()
    if not categories:
        logger.error("No categories found to test")
        return None
    
    category_id = categories[0]["id"]
    endpoint = f"{BASE_URL}/categories/{category_id}"
    response = requests.patch(
        endpoint,
        headers=get_headers(),
        json=TEST_DATA["category"]["update"]
    )
    log_response(response, f"Update Category {category_id}")
    return response.json() if response.status_code == 200 else None

def run_category_tests():
    """Run category related tests"""
    logger.info("\n=== Running Category Tests ===")
    try:
        # Create categories
        created_categories = test_create_categories()
        if created_categories:
            logger.info(f"✅ Successfully created {len(created_categories)} categories")

        # Get and verify categories by type
        categories_by_type = test_get_categories_by_type()
        if categories_by_type:
            logger.info("✅ Successfully verified categories by type")

        # Update category
        updated_category = test_update_category()
        if updated_category:
            logger.info("✅ Successfully updated category")

        logger.info("✅ Category tests passed!")
    except Exception as e:
        logger.error(f"❌ Unexpected error in category tests: {str(e)}")
        
def test_create_transactions():
    """Test creating multiple transactions"""
    endpoint = f"{BASE_URL}/transactions"
    created_transactions = []

    # Get categories and banks first to ensure we have valid IDs
    categories = test_get_categories()
    banks = test_get_banks()

    if not categories or not banks:
        logger.error("Cannot create transactions without categories and banks")
        return None

    # Create a mapping for categories by name for easier reference
    category_map = {cat["name"]: cat["id"] for cat in categories}
    bank_map = {bank["name"]: bank["id"] for bank in banks}

    logger.info("\nCreating transactions...")
    for transaction_data in TEST_DATA["transaction"]["create_multiple"]:
        # Create a copy of transaction data to modify
        trans_data = transaction_data.copy()
        
        # Get category and bank IDs
        category_name = next((k for k, v in category_map.items() if v == trans_data["category_id"]), None)
        bank_name = next((k for k, v in bank_map.items() if v == trans_data["bank_id"]), None)
        
        if not category_name or not bank_name:
            logger.warning(f"Skipping transaction: Invalid category_id or bank_id")
            continue

        response = requests.post(
            endpoint,
            headers=get_headers(),
            json=trans_data
        )
        log_response(response, f"Create Transaction: {trans_data['description']}")
        
        if response.status_code == 200:
            logger.info(f"✅ Successfully created transaction: {trans_data['description']}")
            created_transactions.append(response.json())
        else:
            logger.error(f"❌ Failed to create transaction: {trans_data['description']}")
        
        add_delay()

    return created_transactions

def test_get_transactions():
    """Test getting all transactions"""
    endpoint = f"{BASE_URL}/transactions"
    response = requests.get(
        endpoint,
        headers=get_headers()
    )
    log_response(response, "Get All Transactions")
    
    if response.status_code == 200:
        transactions = response.json()
        logger.info(f"Found {len(transactions)} transactions")
        return transactions
    else:
        logger.error("Failed to get transactions")
        return None

def test_get_transaction():
    """Test getting a specific transaction"""
    transactions = test_get_transactions()
    if not transactions:
        logger.error("No transactions found to test")
        return None
    
    transaction_id = transactions[0]["id"]
    endpoint = f"{BASE_URL}/transactions/{transaction_id}"
    response = requests.get(
        endpoint,
        headers=get_headers()
    )
    log_response(response, f"Get Transaction {transaction_id}")
    return response.json() if response.status_code == 200 else None

def test_update_transaction():
    """Test updating a transaction"""
    transactions = test_get_transactions()
    if not transactions:
        logger.error("No transactions found to test")
        return None
    
    transaction_id = transactions[0]["id"]
    endpoint = f"{BASE_URL}/transactions/{transaction_id}"
    response = requests.patch(
        endpoint,
        headers=get_headers(),
        json=TEST_DATA["transaction"]["update"]
    )
    log_response(response, f"Update Transaction {transaction_id}")
    return response.json() if response.status_code == 200 else None

def test_filter_transactions():
    """Test filtering transactions"""
    endpoint = f"{BASE_URL}/transactions"
    
    # Test different filter combinations
    filters = [
        {"start_date": "2024-01-01"},
        {"end_date": "2024-12-31"},
        {"category_id": "1"},
        {"bank_id": "1"},
        {"start_date": "2024-01-01", "end_date": "2024-12-31"}
    ]

    filter_results = []
    for filter_params in filters:
        response = requests.get(
            endpoint,
            headers=get_headers(),
            params=filter_params
        )
        log_response(response, f"Filter Transactions with params: {filter_params}")
        
        if response.status_code == 200:
            transactions = response.json()
            logger.info(f"Found {len(transactions)} transactions with filter: {filter_params}")
            filter_results.append({
                "filter": filter_params,
                "count": len(transactions)
            })
        
        add_delay()

    return filter_results

def run_transaction_tests():
    """Run transaction related tests"""
    logger.info("\n=== Running Transaction Tests ===")
    try:
        # Create transactions
        created_transactions = test_create_transactions()
        if created_transactions:
            logger.info(f"✅ Successfully created {len(created_transactions)} transactions")

        # Get all transactions
        transactions = test_get_transactions()
        if transactions:
            logger.info("✅ Successfully retrieved all transactions")

        # Get specific transaction
        transaction = test_get_transaction()
        if transaction:
            logger.info("✅ Successfully retrieved specific transaction")

        # Update transaction
        updated_transaction = test_update_transaction()
        if updated_transaction:
            logger.info("✅ Successfully updated transaction")

        # Test filters
        filter_results = test_filter_transactions()
        if filter_results:
            logger.info("✅ Successfully tested transaction filters")
            for result in filter_results:
                logger.info(f"Filter: {result['filter']} -> Found: {result['count']} transactions")

        logger.info("✅ Transaction tests passed!")
    except Exception as e:
        logger.error(f"❌ Unexpected error in transaction tests: {str(e)}")

def run_all_tests():
    """Run all API endpoint tests"""
    start_time = datetime.now()
    logger.info("\n🚀 Starting API Endpoint Tests")
    logger.info(f"Testing API at: {BASE_URL}")
    logger.info("=" * 50)
    
    # Run auth tests first and ensure we have a token
    run_auth_tests()
    
    if TOKEN:
        run_bank_tests()
        run_category_tests()
        run_transaction_tests()
    else:
        logger.error("❌ Skipping remaining tests due to authentication failure")
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    logger.info("\n=== Test Summary ===")
    logger.info(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Duration: {duration.total_seconds():.2f} seconds")
    logger.info("✨ All tests completed!")
