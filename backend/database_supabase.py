import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base

def get_supabase_url():
    """Get Supabase database URL with proper configuration for Render"""
    base_url = os.getenv("DATABASE_URL")
    
    if not base_url:
        # Fallback to individual components
        supabase_host = os.getenv("SUPABASE_HOST", "db.alltdwjhpdtcrsweotgh.supabase.co")
        supabase_user = os.getenv("SUPABASE_USER", "postgres")
        supabase_password = os.getenv("SUPABASE_PASSWORD", "Peterko123!")
        supabase_db = os.getenv("SUPABASE_DB", "postgres")
        supabase_port = os.getenv("SUPABASE_PORT", "5432")
        
        base_url = f"postgresql://{supabase_user}:{supabase_password}@{supabase_host}:{supabase_port}/{supabase_db}"
    
    # Add connection parameters for better compatibility with Render
    if "?" not in base_url:
        base_url += "?"
    else:
        base_url += "&"
    
    # Add parameters for better connection stability
    connection_params = [
        "sslmode=require",
        "connect_timeout=10",
        "application_name=peter-stoyanov-backend"
    ]
    
    return base_url + "&".join(connection_params)

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