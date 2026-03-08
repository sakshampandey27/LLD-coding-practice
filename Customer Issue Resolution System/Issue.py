from enum import Enum
import uuid
from IssueType import IssueType

class IssueStatus(Enum):
    OPEN = 1
    ASSIGNED = 2
    RESOLVED = 3

class Issue:
    def __init__(self, transaction_id, type, subject, description, email):
        self.id = str(uuid.uuid4())
        self.transaction_id = transaction_id
        self.type = IssueType[type.strip().upper()]
        self.subject = subject
        self.description = description
        self.email = email
        self._status = IssueStatus.OPEN
        self.assigned_agent = None
    
    def get_type(self):
        return self.type.name
    
    def is_open(self):
        return self._status == IssueStatus.OPEN
    
    def get_status(self):
        return self._status
    
    def get_email(self):
        return self.email
    
    def get_assigned_agent(self):
        if self.assigned_agent:
            return self.assigned_agent.id
        return None
    
    def get_summary(self):
        return {
            "Type": self.get_type(),
            "Status": self.get_status(),
            "Email": self.get_email(),
            "Subject": self.subject,
            "Description": self.description,
            "Agent": self.get_assigned_agent()
        }
    
    def assign(self, assigned_agent):
        if not self.is_open():
            raise RuntimeError("Issue is not in OPEN status - cannot assign")
        self.assigned_agent = assigned_agent
        self._status = IssueStatus.ASSIGNED
    
    def resolve(self):
        if not self._status == IssueStatus.ASSIGNED:
            raise RuntimeError("Issue is not in ASSIGNED status - cannot resolve")
        self._status = IssueStatus.RESOLVED