import os
import mysql.connector
from mysql.connector import pooling

_db_pool = None


def init_db_pool():
    """
    Initializes the MySQL connection pool.
    Must be called AFTER environment variables are loaded.
    """
    global _db_pool

    if _db_pool is not None:
        return

    db_config = {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
    }

    _db_pool = pooling.MySQLConnectionPool(
        pool_name="ospaat_pool",
        pool_size=5,
        pool_reset_session=True,
        **db_config
    )


def get_db_connection():
    """
    Returns a pooled MySQL connection.
    """
    if _db_pool is None:
        raise RuntimeError("Database pool is not initialized")

    return _db_pool.get_connection()
