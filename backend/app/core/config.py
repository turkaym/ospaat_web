import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

APP_NAME = os.getenv("APP_NAME", "FastAPI App")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
