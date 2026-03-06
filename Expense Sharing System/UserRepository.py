class UserRepository:
    def __init__(self):
        self.users = {}
    
    def save(self, user):
        self.users[user.id] = user
    
    def get(self, user_id):
        if user_id not in self.users:
            raise KeyError("User does not exist")
        return self.users[user_id]
    
    def list(self):
        return list(self.users.values())