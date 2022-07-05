import mysql.connector
from mysql.connector import Error

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

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("資料庫連線已關閉")
