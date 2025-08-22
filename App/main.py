from fastapi import FastAPI
from .database import engine, Base
from .auth.models import User
from .auth.router import router as auth_router
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastAPI User Management",
    description="API quản lý user đơn giản với FastAPI và PostgreSQL",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

@app.on_event("startup")
async def startup_event():
    """Tạo bảng khi khởi động"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}")

app.include_router(auth_router, prefix="/users", tags=["users"])

@app.get("/", tags=["root"])
def root():
    """Root endpoint - Thông tin API"""
    return {
        "message": "FastAPI User Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
