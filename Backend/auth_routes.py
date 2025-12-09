import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from fastapi import HTTPException
from models import UserCreate, UserLogin, UserResponse
from database import get_db_connection
from mysql.connector import Error

SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_super_segura_cambiar_en_produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(user_id: int, email: str) -> str:
    """Crea un token JWT"""
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> dict:
    """Verifica y decodifica un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def register_user_route(user: UserCreate) -> UserResponse:
    """Registra un nuevo usuario"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Verificar si el email ya existe
        cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        
        # Verificar si el username ya existe
        cursor.execute("SELECT id FROM users WHERE username = %s", (user.username,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
        
        # Hashear contraseña
        hashed_password = hash_password(user.password)
        
        # Insertar nuevo usuario
        cursor.execute(
            "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)",
            (user.email, user.username, hashed_password)
        )
        connection.commit()
        user_id = cursor.lastrowid
        
        # Obtener el usuario creado
        cursor.execute("SELECT id, email, username, created_at FROM users WHERE id = %s", (user_id,))
        new_user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        # Crear token
        token = create_access_token(new_user['id'], new_user['email'])
        
        return UserResponse(
            id=new_user['id'],
            email=new_user['email'],
            username=new_user['username'],
            created_at=new_user['created_at'],
            token=token
        )
    except HTTPException:
        raise
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def login_user_route(user: UserLogin) -> UserResponse:
    """Autentica un usuario y retorna un token"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Buscar usuario por email
        cursor.execute("SELECT id, email, username, password, created_at FROM users WHERE email = %s", (user.email,))
        db_user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not db_user or not verify_password(user.password, db_user['password']):
            raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
        
        # Crear token
        token = create_access_token(db_user['id'], db_user['email'])
        
        return UserResponse(
            id=db_user['id'],
            email=db_user['email'],
            username=db_user['username'],
            created_at=db_user['created_at'],
            token=token
        )
    except HTTPException:
        raise
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def verify_user_token_route(token: str) -> dict:
    """Verifica si un token es válido"""
    try:
        payload = verify_token(token)
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, email, username, created_at FROM users WHERE id = %s", (payload['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        return {
            "id": user['id'],
            "email": user['email'],
            "username": user['username'],
            "created_at": user['created_at']
        }
    except HTTPException:
        raise
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
