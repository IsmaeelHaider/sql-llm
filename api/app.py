from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI, **kwargs):
    yield


def get_application() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # setup_sentry(app)

    app.include_router(router=api_router)

    return app
