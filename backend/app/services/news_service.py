from app.utils.audit import log_action


def create_news(db, current_user, data):
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO news (title, summary, content, is_published, is_deleted)
        VALUES (%s, %s, %s, false, false)
        """,
        (data.title, data.summary, data.content)
    )

    news_id = cursor.lastrowid
    db.commit()

    log_action(
        user_id=current_user.id,
        username=current_user.username,
        action="CREATE",
        entity="news",
        entity_id=news_id,
        details="created draft"
    )

    cursor.close()
    return news_id


def update_news(db, current_user, news_id, data):
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE news
        SET title=%s, summary=%s, content=%s, updated_at=NOW()
        WHERE id=%s AND is_deleted=false
        """,
        (data.title, data.summary, data.content, news_id)
    )

    db.commit()

    log_action(
        user_id=current_user.id,
        username=current_user.username,
        action="UPDATE",
        entity="news",
        entity_id=news_id,
        details="updated news"
    )

    cursor.close()
    return True


def set_publish_state(db, current_user, news_id, is_published):
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE news
        SET is_published=%s,
            published_at=IF(%s, NOW(), NULL)
        WHERE id=%s AND is_deleted=false
        """,
        (is_published, is_published, news_id)
    )

    db.commit()

    log_action(
        user_id=current_user.id,
        username=current_user.username,
        action="PUBLISH" if is_published else "UNPUBLISH",
        entity="news",
        entity_id=news_id,
        details="publish toggle"
    )

    cursor.close()
    return True


def soft_delete_news(db, current_user, news_id):
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE news
        SET is_deleted=true, deleted_at=NOW()
        WHERE id=%s
        """,
        (news_id,)
    )

    db.commit()

    log_action(
        user_id=current_user.id,
        username=current_user.username,
        action="DELETE",
        entity="news",
        entity_id=news_id,
        details="soft delete"
    )

    cursor.close()
    return True


def restore_news(db, current_user, news_id):
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE news
        SET is_deleted=false, deleted_at=NULL
        WHERE id=%s
        """,
        (news_id,)
    )

    db.commit()

    log_action(
        user_id=current_user.id,
        username=current_user.username,
        action="RESTORE",
        entity="news",
        entity_id=news_id,
        details="restored news"
    )

    cursor.close()
    return True
