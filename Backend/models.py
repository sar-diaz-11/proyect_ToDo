from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Task(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

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
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

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
    created_at: datetime  # Ahora FastAPI podrá serializarlo correctamente
    token: str
    
    class Config:
        # Esto le dice a Pydantic cómo convertir datetime a JSON
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }