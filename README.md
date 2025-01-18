# FLOO - Financial Logger/Organizer Online

<div align="center">
  <img src="./floo-logo.jpeg" alt="FLOO Logo" width="200"/>
  
  ![Python](https://img.shields.io/badge/python-3.12-blue.svg)
  ![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-green.svg)
  ![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)
  ![License](https://img.shields.io/badge/license-MIT-blue.svg)
</div>

## 📊 Overview

FLOO is a modern financial tracking application that helps users manage their personal finances across multiple bank accounts. Built with FastAPI for the backend and Next.js for the frontend, FLOO provides a seamless experience for tracking expenses, monitoring account balances, and managing financial categories.

## 🌟 Features

- **Multi-Bank Support**: Track balances across different bank accounts
- **Smart Categorization**: Organize transactions with customizable categories
- **Balance Tracking**: Monitor start and end balances for each account
- **Transaction Management**: Record and track both income and expenses
- **Secure Authentication**: JWT-based authentication system
- **Responsive Design**: Mobile-friendly interface

## 🏗️ Project Structure

```
floo/
├── backend/
    ├── app/
    │   ├── __init__.py
    │   ├── api/
    │   ├── core/
    │   ├── db/
    │   └── models/
    ├── tests/
    │   ├── __init__.py
    │   ├── logs/
    │   │   └── test_run_xxxxx
    │   ├── test_endpoints.py
    │   └── test_data.json
    ├── run_tests.py
    ├── venv
    ├── .env
    ├── requirements.txt
    ├── init_db.py
    ├── run_test.py
    └── main.py
│
└── frontend/         # Next.js Frontend (Coming Soon)
```

## 🚀 Technology Stack

### Backend

- **FastAPI**: Modern Python web framework
- **SQLModel**: SQL database interaction
- **PostgreSQL**: Primary database
- **JWT**: Authentication handling
- **Python 3.12**: Core programming language

### Frontend (Coming Soon)

- **Next.js 14**: React framework
- **TypeScript**: Type-safe code
- **Tailwind CSS**: Styling
- **React Query**: State management

## 🛠️ Setup & Installation

### Backend Setup

1. Clone the repository

```bash
git clone https://github.com/yourusername/floo.git
cd floo/backend
```

2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Setup environment variables

```bash
cp .env.example .env
# Edit .env with your configurations
```

5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📝 API Endpoints

### Authentication

- `POST /api/v1/register`: Register new user
- `POST /api/v1/login`: Login user

### Banks

- `GET /api/v1/banks`: List all banks
- `POST /api/v1/banks`: Create new bank
- `PATCH /api/v1/banks/{id}`: Update bank
- `DELETE /api/v1/banks/{id}`: Delete bank

### Categories

- `GET /api/v1/categories`: List all categories
- `POST /api/v1/categories`: Create new category
- `PATCH /api/v1/categories/{id}`: Update category
- `DELETE /api/v1/categories/{id}`: Delete category

### Transactions

- `GET /api/v1/transactions`: List all transactions
- `POST /api/v1/transactions`: Create new transaction
- `PATCH /api/v1/transactions/{id}`: Update transaction
- `DELETE /api/v1/transactions/{id}`: Delete transaction

## 🔒 Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/floo_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 🎢 Testing

Run API endpoint tests:

```bash
# Run all tests
python tests/test_endpoints.py --all

# Run specific tests
python tests/test_endpoints.py --auth    # Authentication tests only
python tests/test_endpoints.py --bank    # Bank tests only
python tests/test_endpoints.py --category # Category tests only
python tests/test_endpoints.py --transaction # Transaction tests only

#To save the log in md file, you can use
python tests/test_endpoints.py --all --format md
#or if you want in txt file, you can use
python tests/test_endpoints.py --all --format txt


## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work - [YourGithub](https://github.com/yourusername)

## 🙏 Acknowledgments

- FastAPI Documentation
- SQLModel Documentation
- Next.js Documentation
- All contributors who help improve this project

---

<div align="center">
  Made with ❤️ by [Your Name]
</div>
```
