from datetime import datetime
import uuid
from enum import Enum

class TaskStatus(Enum):
    CREATED = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4


class Task:
    def __init__(self, function_name, payload, scheduled_time, priority):
        self.id = str(uuid.uuid4())
        self.function_name = function_name
        self.payload = payload
        self.scheduled_time = scheduled_time
        self.priority = priority
        self.created_time = datetime.now()
        self.status = TaskStatus.CREATED

    # def __lt__(self, other):
    #     return (
    #         self.scheduled_time,
    #         self.priority,
    #         self.created_time
    #     ) < (
    #         other.scheduled_time,
    #         other.priority,
    #         other.created_time
    #     )
    
    def set_running(self):
        self.status = TaskStatus.RUNNING
    
    def mark_completed(self):
        self.status = TaskStatus.COMPLETED

    def mark_failed(self):
        self.status = TaskStatus.FAILED
