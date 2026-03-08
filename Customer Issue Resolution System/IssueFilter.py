from IssueType import IssueType
from Issue import IssueStatus

class IssueFilter:
    def __init__(self, type=None, status=None, email=None, agent_id=None):
        self.type = type
        self.status = status
        self.email = email
        self.agent = agent_id
    