import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.db import close_db, init_db


def create_app(*, init_db_on_startup: bool = True) -> FastAPI:
    app = FastAPI(
        title="Route Optimization Solver",
        description="Async wrapper around CVRPTW solver",
        version="1.2.0",
    )

    origins = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    if init_db_on_startup:

        @app.on_event("startup")
        async def startup() -> None:
            await init_db()

        @app.on_event("shutdown")
        async def shutdown() -> None:
            await close_db()

    return app


app = create_app()
