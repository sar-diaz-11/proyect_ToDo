from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de ToDo"}

def get_user_id_from_token(authorization: Optional[str] = Header(None)) -> int:
    """Extrae el user_id del token JWT del header Authorization"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = verify_jwt_token(token)
        return payload.get("user_id")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al verificar token: {str(e)}")
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/tasks", response_model=List[Task])
def get_tasks(completed: Optional[bool] = None, priority: Optional[str] = None, authorization: Optional[str] = Header(None)):
    user_id = get_user_id_from_token(authorization)
    return get_tasks_route(user_id, completed, priority)

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, authorization: Optional[str] = Header(None)):
    user_id = get_user_id_from_token(authorization)
    return create_task_route(user_id, task)

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, authorization: Optional[str] = Header(None)):
    user_id = get_user_id_from_token(authorization)
    return get_task_route(user_id, task_id)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, authorization: Optional[str] = Header(None)):
    user_id = get_user_id_from_token(authorization)
    return update_task_route(user_id, task_id, task)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, authorization: Optional[str] = Header(None)):
    user_id = get_user_id_from_token(authorization)
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