from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="0.1.0",
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}