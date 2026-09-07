from fastapi import FastAPI

from app.api.search import router as search_router
from app.api.ask import router as ask_router
from app.api.investigate import router as investigate_router


app = FastAPI(
    title="OpsIntel API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "OpsIntel API is running"}


app.include_router(
    search_router,
    prefix="/api",
)

app.include_router(
    ask_router,
    prefix="/api",
)

app.include_router(
    investigate_router,
    prefix="/api",
)
