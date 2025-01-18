from datetime import datetime

from tests.test_endpoints import TOKEN, generate_markdown_report, run_all_tests, run_auth_tests, run_bank_tests, run_category_tests, run_transaction_tests, setup_logging


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test FLOO API endpoints')
    parser.add_argument('--auth', action='store_true', help='Run only authentication tests')
    parser.add_argument('--bank', action='store_true', help='Run only bank tests')
    parser.add_argument('--category', action='store_true', help='Run only category tests')
    parser.add_argument('--transaction', action='store_true', help='Run only transaction tests')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--format', choices=['log', 'txt', 'md'], default='log',
                       help='Output format for the report')
    
    args = parser.parse_args()
    
    try:
        # Setup logging
        log_filename, logger = setup_logging()
        
        # Store start time
        start_time = datetime.now()
        logger.info(f"Test session started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if args.auth:
            run_auth_tests()
        elif args.bank:
            run_auth_tests()
            if TOKEN:
                run_bank_tests()
        elif args.category:
            run_auth_tests()
            if TOKEN:
                run_category_tests()
        elif args.transaction:
            run_auth_tests()
            if TOKEN:
                run_transaction_tests()
        else:
            run_all_tests()
        
        # Calculate duration
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"\nTest session completed in {duration.total_seconds():.2f} seconds")
            
        # Generate report in requested format
        if args.format == 'md':
            md_filename = generate_markdown_report(log_filename)
            logger.info(f"Markdown report generated: {md_filename}")
        elif args.format == 'txt':
            txt_filename = log_filename.replace('.log', '.txt')
            import shutil
            shutil.copy(log_filename, txt_filename)
            logger.info(f"Text report generated: {txt_filename}")
            
        logger.info(f"Log file saved: {log_filename}")
            
    except KeyboardInterrupt:
        logger.info("\n⚠️ Tests interrupted by user")
    except Exception as e:
        logger.error(f"\n❌ Tests failed with error: {str(e)}")
        raise
    finally:
        logger.info("\n👋 Test session ended")
