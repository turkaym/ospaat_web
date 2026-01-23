import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.core.database import init_db_pool, get_db_connection
from app.routes.auth import router as auth_router
from app.routes.news import router as news_router
from app.routes.admin import router as admin_router
from app.routes.news_admin import router as news_admin_router
from dotenv import load_dotenv
load_dotenv()


ENV = os.getenv("ENV", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(
    title="OSP AAT API",
    version="0.1.0",
    debug=DEBUG,
)


origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(news_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(news_admin_router)


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
