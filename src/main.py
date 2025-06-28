from fastapi import FastAPI, Response
from pydantic import BaseSettings
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()
app = FastAPI()

REQUEST_COUNT = Counter("request_count", "Total HTTP requests")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.get("/")
async def root():
    REQUEST_COUNT.inc()
    return {"message": "Hello from {{ service_name }}"}
