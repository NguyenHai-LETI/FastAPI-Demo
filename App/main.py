from fastapi import FastAPI
from .database import engine, Base
from .auth.models import User
from .auth.router import router as auth_router
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Khởi tạo ứng dụng và các trờng cơ bản
app = FastAPI(
    title="FastAPI demo",
    description="Demo using FastAPI",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    """Trong dự án thực tế startup chỉ để:
    1. tạo kết nối tới service bên ngoài: redis, rabbitmq
    2. pre-load dữ lieu người dùng, cấu hình log monitorring
    3. Kiểm tra kết nối db: ping db, check pool connection, KHÔNG TẠO/TƯƠNG TÁC DB"""
    try:
        Base.metadata.create_all(bind=engine) # tạo mọi bảng được khai báo
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}")

#thẻ tags để phân nhóm docs/swagger
app.include_router(auth_router, prefix="/users", tags=["users"])

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Hello FastAPI"}
