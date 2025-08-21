import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base

# Simple Supabase direct connection with SSL
SUPABASE_URL = "postgresql://postgres:Peterko123!@db.alltdwjhpdtcrsweotgh.supabase.co:5432/postgres?sslmode=require"

def get_supabase_url():
    """Get Supabase database URL for Render"""
    return os.getenv("DATABASE_URL", SUPABASE_URL)

# Get database URL with proper configuration
DATABASE_URL = get_supabase_url()

print(f"🔗 Connecting to database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'unknown'}")

# Create SQLAlchemy engine with connection pool settings
engine = create_engine(
    DATABASE_URL,
    # Connection pool settings for better reliability
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    # Connect args for PostgreSQL
    connect_args={
        "connect_timeout": 10,
        "application_name": "peter-stoyanov-backend"
    }
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get the database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test connection and create tables
try:
    print("📋 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    # Don't fail startup, just log the error
    pass