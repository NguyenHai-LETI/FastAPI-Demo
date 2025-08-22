#!/usr/bin/env python3
"""
File để chạy trực tiếp từ thư mục App
"""
import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Khởi động FastAPI User Management Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔗 Server URL: http://localhost:8000")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
