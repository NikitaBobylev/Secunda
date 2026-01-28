from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.logging import setup_logging

def on_startup():
    setup_logging()

app = FastAPI(
    title="Secunda Directory API",
    description=(
        "REST API для справочника организаций, зданий и видов деятельности.\n\n"
        "Все запросы требуют заголовок `X-API-Key` со статическим ключом."
    ),
    version="0.1.0",
    on_startup=[on_startup]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")
