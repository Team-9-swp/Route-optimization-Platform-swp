import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Route Optimization Solver",
        description="Async wrapper around main_mvp.py CVRPTW solver",
        version="1.1.0",
    )

    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app


app = create_app()
