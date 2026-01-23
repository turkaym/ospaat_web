from datetime import datetime
from app.core.database import get_db_connection


def log_action(
    *,
    user_id: int,
    username: str,
    action: str,
    entity: str,
    entity_id: int | None = None,
    details: str | None = None
) -> None:
    """
    Registra una acción sensible en audit_logs.
    Nunca debe romper el flujo principal.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO audit_logs
            (user_id, username, action, entity, entity_id, details, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                username,
                action,
                entity,
                entity_id,
                details,
                datetime.utcnow(),
            )
        )

        conn.commit()

    except Exception as e:
        print(f"[AUDIT ERROR] {e}")

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass
