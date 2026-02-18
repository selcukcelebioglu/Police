from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Vatandaş odaklı AI trafik ihlali ön raporlama sistemi",
    version="1.0.0",
)

app.include_router(router, prefix=settings.api_prefix)


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
