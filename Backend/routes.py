from fastapi import HTTPException
from models import Task, TaskCreate, TaskUpdate
from database import get_db_connection
from mysql.connector import Error
from typing import List, Optional
from datetime import datetime
import logging
import traceback

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_datetime(dt):
    """Convierte datetime a string ISO de forma segura"""
    if dt is None:
        return datetime.utcnow().isoformat()
    if isinstance(dt, datetime):
        return dt.isoformat()
    if isinstance(dt, str):
        return dt
    return str(dt)

def get_tasks_route(user_id: int, completed: Optional[bool] = None, priority: Optional[str] = None) -> List[Task]:
    """Obtiene todas las tareas del usuario con filtros opcionales"""
    try:
        logger.info(f"📋 Obteniendo tareas para user_id: {user_id}")
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
        
        query += " ORDER BY created_at DESC"
        
        logger.info(f"Query: {query}, Params: {params}")
        cursor.execute(query, tuple(params))
        tasks = cursor.fetchall()
        logger.info(f"✅ Tareas encontradas: {len(tasks)}")
        
        cursor.close()
        connection.close()
        
        # Convertir datetime a string
        for task in tasks:
            logger.info(f"Procesando tarea ID: {task.get('id')}")
            task['created_at'] = format_datetime(task.get('created_at'))
            task['updated_at'] = format_datetime(task.get('updated_at'))
        
        return [Task(**task) for task in tasks]
    except Exception as e:
        logger.error(f"❌ Error en get_tasks_route: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al obtener tareas: {str(e)}")

def create_task_route(user_id: int, task: TaskCreate) -> Task:
    """Crea una nueva tarea"""
    try:
        logger.info(f"📝 Creando tarea para user_id: {user_id}, título: {task.title}")
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(
            """INSERT INTO tasks (user_id, title, description, priority, due_date) 
               VALUES (%s, %s, %s, %s, %s)""",
            (user_id, task.title, task.description, task.priority, task.due_date)
        )
        connection.commit()
        task_id = cursor.lastrowid
        logger.info(f"✅ Tarea creada con ID: {task_id}")
        
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        new_task = cursor.fetchone()
        logger.info(f"Tarea recuperada: {new_task}")
        
        cursor.close()
        connection.close()
        
        # Convertir datetime a string
        new_task['created_at'] = format_datetime(new_task.get('created_at'))
        new_task['updated_at'] = format_datetime(new_task.get('updated_at'))
        
        logger.info(f"Tarea formateada: {new_task}")
        return Task(**new_task)
    except Exception as e:
        logger.error(f"❌ Error en create_task_route: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al crear tarea: {str(e)}")

def get_task_route(user_id: int, task_id: int) -> Task:
    """Obtiene una tarea específica"""
    try:
        logger.info(f"🔍 Buscando tarea {task_id} para user_id: {user_id}")
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        task = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        # Convertir datetime a string
        task['created_at'] = format_datetime(task.get('created_at'))
        task['updated_at'] = format_datetime(task.get('updated_at'))
        
        logger.info(f"✅ Tarea encontrada: {task}")
        return Task(**task)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error en get_task_route: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al obtener tarea: {str(e)}")

def update_task_route(user_id: int, task_id: int, task: TaskUpdate) -> Task:
    """Actualiza una tarea existente"""
    try:
        logger.info(f"✏️ Actualizando tarea {task_id} para user_id: {user_id}")
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Verificar que la tarea existe y pertenece al usuario
        cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        existing_task = cursor.fetchone()
        
        if not existing_task:
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        # Construir query dinámicamente solo con campos proporcionados
        update_fields = []
        params = []
        
        if task.title is not None:
            update_fields.append("title = %s")
            params.append(task.title)
        
        if task.description is not None:
            update_fields.append("description = %s")
            params.append(task.description)
        
        if task.completed is not None:
            update_fields.append("completed = %s")
            params.append(task.completed)
        
        if task.priority is not None:
            update_fields.append("priority = %s")
            params.append(task.priority)
        
        if task.due_date is not None:
            update_fields.append("due_date = %s")
            params.append(task.due_date)
        
        if update_fields:
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = %s AND user_id = %s"
            params.extend([task_id, user_id])
            
            cursor.execute(query, tuple(params))
            connection.commit()
        
        # Obtener tarea actualizada
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        updated_task = cursor.fetchone()
        cursor.close()
        connection.close()
        
        # Convertir datetime a string
        updated_task['created_at'] = format_datetime(updated_task.get('created_at'))
        updated_task['updated_at'] = format_datetime(updated_task.get('updated_at'))
        
        logger.info(f"✅ Tarea actualizada: {updated_task}")
        return Task(**updated_task)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error en update_task_route: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al actualizar tarea: {str(e)}")

def delete_task_route(user_id: int, task_id: int) -> dict:
    """Elimina una tarea"""
    try:
        logger.info(f"🗑️ Eliminando tarea {task_id} para user_id: {user_id}")
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Verificar que la tarea existe y pertenece al usuario
        cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        task = cursor.fetchone()
        
        if not task:
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        connection.commit()
        cursor.close()
        connection.close()
        
        logger.info(f"✅ Tarea eliminada exitosamente")
        return {"message": "Tarea eliminada exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error en delete_task_route: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al eliminar tarea: {str(e)}")