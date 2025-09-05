from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as api_router
from .core.config import BACKEND_ALLOWED_ORIGINS


def create_app() -> FastAPI:
    app = FastAPI(title="AI Extension Backend")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if BACKEND_ALLOWED_ORIGINS == "*" else BACKEND_ALLOWED_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    return app


app = create_app()
