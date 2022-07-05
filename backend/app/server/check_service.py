from datetime import datetime, timedelta, timezone
import mysql.connector
from mysql.connector import Error
from flask import current_app

from app.config import SQLALCHEMY_DATABASE_URI


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
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='140.133.74.170',          # 主機名稱
            database='bas',  # 資料庫名稱
            user='italab',        # 帳號
            password='ma308')  # 密碼

        if connection.is_connected():

            # 顯示資料庫版本
            db_Info = connection.get_server_info()
            print("資料庫版本：", db_Info)

            # 顯示目前使用的資料庫
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("目前使用的資料庫：", record)

    except Error as e:
        print("資料庫連接失敗：", e)
        current_app.logger.error({'sql': e})
        return status
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
            status["isAlive"] = True
            return status
