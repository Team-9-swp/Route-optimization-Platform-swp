from fastapi import FastAPI

from app.api import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Route Optimization Solver",
        description="Async wrapper around main_mvp.py CVRPTW solver",
        version="0.1.0",
    )
    app.include_router(router)
    return app


app = create_app()
