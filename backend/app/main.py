# =========================
# Load environment variables FIRST
# =========================
from app.core.database import init_db_pool, get_db_connection
from app.routes.auth import router as auth_router
from app.routes.news import router as news_router
from app.routes.admin import router as admin_router  # De prueba
from app.routes.news_admin import router as news_admin_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
from dotenv import load_dotenv
load_dotenv()


# =========================
# Environment
# =========================
ENV = os.getenv("ENV", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(
    title="OSP AAT API",
    version="0.1.0",
    debug=DEBUG,
)

# =========================
# CORS
# =========================
origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Routers
# =========================
app.include_router(news_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(news_admin_router)


# =========================
# Startup – DB check
# =========================


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

# =========================
# Root
# =========================


@app.get("/")
def root():
    return {
        "project": "OSP AAT",
        "status": "backend running",
        "environment": ENV,
    }
