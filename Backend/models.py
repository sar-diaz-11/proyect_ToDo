from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[str] = None
    created_at: str  # ⚠️ Cambiado de datetime a str
    updated_at: str  # ⚠️ Cambiado de datetime a str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None

class User(BaseModel):
    id: int
    email: str
    username: str
    created_at: str  # ⚠️ Cambiado de datetime a str

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: str
    token: str