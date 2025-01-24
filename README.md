# Floo Project

## Recent Changes: User Data Isolation

All data (categories, banks, and transactions) is now user-specific. Each user can only access and modify their own data.

### Database Changes

- Added `user_id` foreign key to categories and banks tables
- Added relationships between User and all other models
- Added database indexes for performance optimization
- Updated API endpoints to handle user-specific data access

### Running Database Migrations

To apply the new changes to your database:

```bash
# From the backend directory
python -c "from app.db.migrations import run_migrations; run_migrations()"
```

This will:

1. Add user_id columns to necessary tables
2. Create foreign key constraints
3. Create performance indexes
4. Make user_id required for all tables

### Security Features

- All API endpoints now verify user ownership of data
- Proper error handling for unauthorized access attempts
- Database-level foreign key constraints
- API-level authorization checks

### API Changes

All endpoints now:

- Require authentication
- Filter data by current user
- Verify ownership before modifications
- Include user_id in responses

Example endpoints:

- GET /api/v1/categories - Returns only current user's categories
- POST /api/v1/banks - Automatically associates new bank with current user
- PATCH /api/v1/transactions/{id} - Verifies transaction ownership before update

### Model Updates

Updated models:

- Category: Added user relationship
- Bank: Added user relationship
- User: Added relationships to all models
- Transaction: Already had user relationship
