from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Task, TaskCreate, TaskUpdate
from routes import (
    get_tasks_route,
    create_task_route,
    get_task_route,
    update_task_route,
    delete_task_route
)
from typing import List, Optional

app = FastAPI(title="Todo API")

# Configurar CORS para React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://effulgent-praline-3c31f9.netlify.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de ToDo"}

@app.get("/tasks", response_model=List[Task])
def get_tasks(completed: Optional[bool] = None, priority: Optional[str] = None):
    return get_tasks_route(completed, priority)

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    return create_task_route(task)

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    return get_task_route(task_id)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    return update_task_route(task_id, task)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return delete_task_route(task_id)