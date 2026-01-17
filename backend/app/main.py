from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.core.database import init_db_pool, get_db_connection


# =========================
# Load environment variables
# =========================
load_dotenv()

ENV = os.getenv("ENV", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(
    title="OSP AAT API",
    version="0.1.0",
    debug=DEBUG,
)


@app.on_event("startup")
def startup_event():
    try:
        init_db_pool()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()

        print("✅ Database connection successful")

    except Exception as e:
        print("❌ Database connection failed")
        print(e)
        raise


@app.get("/")
def root():
    return {
        "project": "OSP AAT",
        "status": "backend running",
        "environment": ENV,
    }
