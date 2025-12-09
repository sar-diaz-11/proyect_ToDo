import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_db_connection():
    try:
        # Debug: Imprimir la configuración
        print(f"Intentando conectar con: {DB_CONFIG}")
        print(f"Tipo de puerto: {type(DB_CONFIG['port'])}")
        
        # Asegurar que el puerto sea int
        db_config = DB_CONFIG.copy()
        db_config['port'] = int(db_config['port'])
        
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error al conectar a la BD: {e}")
        raise