import requests
import json
import logging
import time
import argparse
from datetime import datetime
from sqlmodel import Session, select
from app.models.user import User
from app.db.session import engine

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run API endpoint tests')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--format', choices=['txt', 'md'], default='txt', help='Output format')
    return parser.parse_args()

class TestLogger:
    def __init__(self):
        self.logger = None
        self.log_filename = None
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args = parse_arguments()
        log_extension = "md" if args.format == "md" else "txt"
        self.log_filename = f"tests/logs/test_run_{timestamp}.{log_extension}"
        
        # Create logs directory if not exists
        import os
        os.makedirs("tests/logs", exist_ok=True)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Setup file handler
        file_handler = logging.FileHandler(self.log_filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Setup logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Remove any existing handlers
        self.logger.handlers = []
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Log initial message
        self.logger.info("=== FLOO API Test Session Started ===")
        self.logger.info(f"Log file created at: {self.log_filename}")

    def generate_markdown_report(self):
        """Generate markdown report from log file"""
        if not self.log_filename:
            return
            
        with open(self.log_filename, 'r') as log_file:
            log_content = log_file.readlines()
        
        with open(self.log_filename, 'w') as md_file:
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

# Constants
BASE_URL = "http://localhost:8000/api/v1"
TOKEN = None
TEST_USER_ID = None

# Global test logger instance
test_logger = TestLogger()
logger = test_logger.logger

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
    """Remove test users and their associated data if exist"""
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
    global TEST_USER_ID
    endpoint = f"{BASE_URL}/register"
    registered_users = []

    for user_data in TEST_DATA["user"]["register_multiple"]:
        response = requests.post(endpoint, json=user_data)
        log_response(response, f"Register User: {user_data['username']}")
        
        if response.status_code == 200:
            logger.info(f"✅ Registration successful for {user_data['username']}")
            registered_users.append(response.json())
            if user_data['username'] == TEST_DATA["user"]["login"]["username"]:
                TEST_USER_ID = response.json()["id"]
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

def run_all_tests():
    """Run all API endpoint tests"""
    start_time = datetime.now()
    logger.info("\n🚀 Starting API Endpoint Tests")
    logger.info(f"Testing API at: {BASE_URL}")
    logger.info("=" * 50)
    
    # Run auth tests first and ensure we have a token
    run_auth_tests()

    end_time = datetime.now()
    duration = end_time - start_time
    
    logger.info("\n=== Test Summary ===")
    logger.info(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Duration: {duration.total_seconds():.2f} seconds")
    logger.info("✨ All tests completed!")

    # Generate markdown report if requested
    args = parse_arguments()
    if args.format == 'md':
        test_logger.generate_markdown_report()

if __name__ == "__main__":
    run_all_tests()
