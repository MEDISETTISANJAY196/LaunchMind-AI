from app.models.notification import Notification


def create_notification(db, user_id, message):
    notification = Notification(
        user_id=user_id,
        message=message,
    )

    db.add(notification)
    db.commit()