from fastapi import FastAPI
from core.config import settings
from api.v1.routes import user
from core.database import test_connection


def create_app() -> FastAPI:
    """
        Tạo instance FastAPI, include các router, cấu hình settings, ...
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0"
    )

    # include các  routers
    app.include_router(user.router, prefix="/api/v1/users", tags=["users"])

    @app.on_event("startup")
    def startup_event():
        print("🔌 Testing database connection...")
        test_connection()

    return app


app = create_app()
