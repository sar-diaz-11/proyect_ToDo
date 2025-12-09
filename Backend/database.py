import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_db_connection():
    try:
        db_config = {
            "host": DB_CONFIG["host"],
            "user": DB_CONFIG["user"],
            "password": DB_CONFIG["password"],
            "database": DB_CONFIG["database"],
            "port": int(DB_CONFIG["port"]) if isinstance(DB_CONFIG["port"], str) else DB_CONFIG["port"]
        }
        
        print(f"DEBUG - Conectando con host: {db_config['host']}, port: {db_config['port']} (tipo: {type(db_config['port'])})")
        
        connection = mysql.connector.connect(**db_config)
        print("Conexión exitosa a la BD")
        return connection
    except Error as e:
        print(f"Error al conectar a la BD: {e}")
        raise