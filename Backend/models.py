from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    id: int
    user_id: int
    title: str
    description: str = None
    completed: bool = False
    priority: str = "medium"
    due_date: str = None
    created_at: datetime
    updated_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: str = None
    priority: str = "medium"
    due_date: str = None

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None
    priority: str = None
    due_date: str = None

class User(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

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
    created_at: datetime
    token: str