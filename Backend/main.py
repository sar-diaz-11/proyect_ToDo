from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import Task, TaskCreate, TaskUpdate, UserCreate, UserLogin, UserResponse
from routes import (
    get_tasks_route,
    create_task_route,
    get_task_route,
    update_task_route,
    delete_task_route
)
from auth_routes import (
    register_user_route,
    login_user_route,
    verify_user_token_route,
    verify_token as verify_jwt_token
)
from typing import List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Todo API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://effulgent-praline-3c31f9.netlify.app",
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar seguridad Bearer
security = HTTPBearer()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de ToDo"}

def get_user_id_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Extrae el user_id del token JWT del header Authorization"""
    try:
        token = credentials.credentials
        payload = verify_jwt_token(token)
        user_id = payload.get("user_id")
        
        if not user_id:
            logger.error("Token no contiene user_id")
            raise HTTPException(status_code=401, detail="Token inválido")
        
        logger.info(f"✅ Token válido para user_id: {user_id}")
        return user_id
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error al verificar token: {str(e)}")
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# ===== RUTAS DE TAREAS =====

@app.get("/tasks", response_model=List[Task])
def get_tasks(
    completed: Optional[bool] = None, 
    priority: Optional[str] = None,
    user_id: int = Depends(get_user_id_from_token)
):
    return get_tasks_route(user_id, completed, priority)

@app.post("/tasks", response_model=Task)
def create_task(
    task: TaskCreate,
    user_id: int = Depends(get_user_id_from_token)
):
    try:
        logger.info(f"📝 Creando tarea para user_id: {user_id}")
        result = create_task_route(user_id, task)
        logger.info(f"✅ Tarea creada exitosamente")
        return result
    except Exception as e:
        logger.error(f"❌ Error al crear tarea: {str(e)}")
        raise

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    user_id: int = Depends(get_user_id_from_token)
):
    return get_task_route(user_id, task_id)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int, 
    task: TaskUpdate,
    user_id: int = Depends(get_user_id_from_token)
):
    return update_task_route(user_id, task_id, task)

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    user_id: int = Depends(get_user_id_from_token)
):
    return delete_task_route(user_id, task_id)

# ===== RUTAS DE AUTENTICACIÓN =====

@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate):
    try:
        logger.info(f"📨 Intento de registro para: {user.email}")
        result = register_user_route(user)
        logger.info(f"✅ Usuario registrado exitosamente: ID {result.id}")
        return result
    except HTTPException as e:
        logger.error(f"❌ HTTPException en registro: {e.status_code} - {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"❌ Error inesperado en registro: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/auth/login", response_model=UserResponse)
def login(user: UserLogin):
    try:
        logger.info(f"📨 Intento de login para: {user.email}")
        result = login_user_route(user)
        logger.info(f"✅ Login exitoso: {user.email}")
        return result
    except HTTPException as e:
        logger.error(f"❌ HTTPException en login: {e.status_code} - {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"❌ Error inesperado en login: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/auth/verify")
def verify_user_token_endpoint(token: str):
    try:
        return verify_user_token_route(token)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"❌ Error en verificación de token: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fix-database")
def fix_database():
    """Endpoint temporal para arreglar la tabla tasks"""
    try:
        from database import get_db_connection
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Arreglar la columna completed para que tenga valor por defecto FALSE
        cursor.execute("""
            ALTER TABLE tasks 
            MODIFY COLUMN completed BOOLEAN NOT NULL DEFAULT FALSE
        """)
        
        # También arreglar created_at y updated_at si tienen NULL
        cursor.execute("""
            ALTER TABLE tasks 
            MODIFY COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        """)
        
        cursor.execute("""
            ALTER TABLE tasks 
            MODIFY COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": "Columnas arregladas exitosamente"}
    except Exception as e:
        return {"error": str(e)}