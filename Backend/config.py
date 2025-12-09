from dotenv import load_dotenv
import os

load_dotenv()

# Función helper para convertir el puerto de forma segura
def get_port():
    port = os.getenv("DB_PORT", "3306")
    try:
        return int(port)
    except (ValueError, TypeError):
        return 3306

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "todo_db"),
    "port": get_port(),
}
