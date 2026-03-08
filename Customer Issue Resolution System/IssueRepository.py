class IssueRepository:
    def __init__(self):
        self.issues = {}
    
    def save(self, issue):
        self.issues[issue.id] = issue
    
    def get(self, issue_id):
        if issue_id not in self.issues:
            raise KeyError("Issue not found")
        return self.issues[issue_id]
    
    def list(self):
        return list(self.issues.values())