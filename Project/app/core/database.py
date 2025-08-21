"""file cấu hình db, session, engine"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # = Project/app
# Lùi ra gốc repo (nơi chứa envs/)
ROOT_DIR = BASE_DIR.parent  # = Project
# Path tới env.develop
env_path = ROOT_DIR.parent / "envs" / ".env.develop"

# Load biến môi trường từ file .env
load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")  # Lấy từ file .env

engine = create_engine(DATABASE_URL, echo=True) #đối tượng kết nối SQLAlchemy và DB

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Factory tạo ra section

Base = declarative_base() # class cha cho tất cả các model SQLAlchemy

# Dependency cho FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful:", result.scalar())
    except Exception as e:
        print("❌ Database connection failed:", e)

# Gọi test khi chạy trực tiếp file
if __name__ == "__main__":
    test_connection()