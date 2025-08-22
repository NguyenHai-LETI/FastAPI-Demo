from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .config import settings

def create_database_url():
    """Tạo DATABASE_URL từ các biến môi trường riêng lẻ"""
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    else:
        return f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Tạo database engine
database_url = create_database_url()
engine = create_engine(
    database_url, 
    echo=False,  # Tắt SQL logging
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency injection khi route gọi
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise
    finally:
        db.close()
