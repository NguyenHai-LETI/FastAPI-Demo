from fastapi import FastAPI
from App.auth import router as auth_router
from App.database import engine, Base

# Tạo bảng khi chạy lần đầu
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Auth Example")

app.include_router(auth_router.router)

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
