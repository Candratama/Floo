from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import init_db
from app.api.v1 import auth, users, banks, categories, transactions
import pyfiglet
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create ASCII art for FLOO
ascii_banner = pyfiglet.figlet_format("FLOO API", font="slant")
print("\n\033[92m" + ascii_banner + "\033[0m")  # \033[92m untuk warna hijau, \033[0m untuk reset warna
print("\033[94m=== Financial Logger/Organizer Online ===\033[0m\n")  # \033[94m untuk warna biru

app = FastAPI(
    title="FLOO API",
    description="Financial Logger/Organizer Online API",
    version="1.0.0"
)

# CORS middleware configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
# @app.on_event("startup")
# def on_startup():
#     logger.info("Initializing database...")
#     init_db()
#     logger.info("Database initialized successfully!")

# Include routers
app.include_router(auth, prefix="/api/v1", tags=["auth"])
app.include_router(users, prefix="/api/v1/users", tags=["users"])
app.include_router(banks, prefix="/api/v1/banks", tags=["banks"])
app.include_router(categories, prefix="/api/v1/categories", tags=["categories"])
app.include_router(transactions, prefix="/api/v1/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {
        "app_name": "FLOO API",
        "version": "1.0.0",
        "status": "running"
    }