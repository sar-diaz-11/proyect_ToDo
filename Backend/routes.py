from fastapi import HTTPException
from typing import List, Optional
from models import Task, TaskCreate, TaskUpdate
from database import get_db_connection
from mysql.connector import Error

def get_tasks_route(user_id: int, completed: Optional[bool] = None, priority: Optional[str] = None) -> List[Task]:
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT * FROM tasks WHERE user_id = %s"
        params = [user_id]
        
        if completed is not None:
            query += " AND completed = %s"
            params.append(completed)
        
        if priority:
            query += " AND priority = %s"
            params.append(priority)
        
        query += " ORDER BY due_date ASC, created_at DESC"
        
        cursor.execute(query, params)
        tasks = cursor.fetchall()
        cursor.close()
        connection.close()
        return tasks
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_task_route(user_id: int, task: TaskCreate) -> Task:
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO tasks (user_id, title, description, priority, due_date) VALUES (%s, %s, %s, %s, %s)",
            (user_id, task.title, task.description, task.priority, task.due_date)
        )
        connection.commit()
        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        new_task = cursor.fetchone()
        cursor.close()
        connection.close()
        return new_task
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_task_route(user_id: int, task_id: int) -> Task:
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        task = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return task
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_task_route(user_id: int, task_id: int, task: TaskUpdate) -> Task:
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        update_fields = []
        values = []
        if task.title is not None:
            update_fields.append("title = %s")
            values.append(task.title)
        if task.description is not None:
            update_fields.append("description = %s")
            values.append(task.description)
        if task.completed is not None:
            update_fields.append("completed = %s")
            values.append(task.completed)
        if task.priority is not None:
            update_fields.append("priority = %s")
            values.append(task.priority)
        if task.due_date is not None:
            update_fields.append("due_date = %s")
            values.append(task.due_date)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        values.append(task_id)
        values.append(user_id)
        query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = %s AND user_id = %s"
        cursor.execute(query, values)
        connection.commit()
        
        cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        updated_task = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not updated_task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return updated_task
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_task_route(user_id: int, task_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        cursor.close()
        connection.close()
        return {"message": "Tarea eliminada correctamente"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))