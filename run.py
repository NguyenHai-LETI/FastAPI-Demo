#!/usr/bin/env python3
"""
Script để chạy FastAPI server
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Khởi động FastAPI User Management Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔗 Server URL: http://localhost:8000")
    print("=" * 50)
    
    uvicorn.run(
        "App.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
