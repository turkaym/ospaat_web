from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import CORS_ORIGINS, APP_NAME, DEBUG

app = FastAPI(
    title=APP_NAME,
    debug=DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def healthcheck():
    return {
        "status": "ok",
        "service": APP_NAME
    }
