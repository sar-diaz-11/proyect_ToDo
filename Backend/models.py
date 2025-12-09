from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import date, datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[date] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    @field_serializer('due_date', when_used='json')
    def serialize_due_date(self, value):
        if value is None:
            return None
        return value.isoformat() if isinstance(value, date) else value

    @field_serializer('created_at', 'updated_at', when_used='json')
    def serialize_datetime(self, value):
        return value.isoformat() if isinstance(value, datetime) else value