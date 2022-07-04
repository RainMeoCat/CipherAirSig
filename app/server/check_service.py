from datetime import datetime, timedelta, timezone

import psycopg2
from flask import current_app

from app.config import SQLALCHEMY_DATABASE_URI
from app.helper import mail


def check_database():
    """Check database connect status

    Returns:
        json: {
        "service": "database",
        "isAlive": bool,
        "description": "資料庫連線狀態"
    }
    """
    status = {
        "service": "database",
        "isAlive": False,
        "description": "資料庫連線狀態"
    }
    try:
        conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
        conn.close()
        status["isAlive"] = True
        return status
    except psycopg2.OperationalError as ex:
        current_app.logger.error({'sql': ex})
        return status


def check_email_service():
    """Check email service status

    Returns:
        json: {
        "service": "email",
        "isAlive": bool,
        "description": "電子信箱服務狀態"
    }
    """
    update_time = datetime.utcnow().astimezone(
        timezone(offset=timedelta(hours=8))).isoformat()

    subject = 'Mail service checkout'
    message = 'flask-mail 啟動訊息 <br> ISO 8601 CheckTime:{} <br> UTC NOW CheckTime:{}'.format(
        update_time, datetime.now())
    mail_to = current_app.config['MAIL_USERNAME']
    send_status = mail.send_email(mail_message=message, subject=subject,
                                  to=mail_to, sync=False)
    status = {
        "service": "email",
        "isAlive": send_status,
        "description": "電子信箱服務狀態"
    }

    return status
