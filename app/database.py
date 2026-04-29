import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="mysql_db",
        user="admin",
        password="admin123",
        database="inventario_db",
        port=3306
    )
    return connection
