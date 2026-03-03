from enum import Enum
from datetime import datetime

class Status(Enum):
    TODO = 1
    INPROGRESS = 2
    COMPLETED = 3

class Task:
    def __init__(self, uuid, title, description=None):
        self.id = uuid
        if not title:
            raise ValueError("Empty title not allowed")
        self.title = title
        self.description = description
        self.status = Status.TODO
        self.created_at = datetime.now()
        self.assigned_user = None        
    
    def get_status(self):
        return self.status
    
    def get_assigned_user(self):
        return self.assigned_user
    
    def update_status(self, new_status):
        try:
            self.status = Status[new_status]
        except Exception as _:
            raise ValueError("Update status failed - new status is not a valid choice")

    def assign_user(self, user):
        if not user:
            raise ValueError("User cannot be empty")
        self.assigned_user = user
    
    def get_summary(self):
        return {
            "ID": self.id,
            "Title": self.title,
            "Description": self.description,
            "Created_at": self.created_at,
            "Assigned_user": self.assigned_user,
            "Status": self.status
        }