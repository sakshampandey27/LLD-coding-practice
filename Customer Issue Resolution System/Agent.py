class Agent:
    def __init__(self, id, email, expertise):
        self.id = id
        self.email = email
        self.expertise = set(expertise)
        self.active_issues = []
    
    def get_expertise(self):
        return self.expertise
    
    def get_active_issues_count(self):
        return len(self.active_issues)
    
    def add_new_issue(self, issue_id):
        if issue_id:
            self.active_issues.append(issue_id)
    
    def resolve_issue(self, issue_id):
        if issue_id:
            self.active_issues.remove(issue_id)