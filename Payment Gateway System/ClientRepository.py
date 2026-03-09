class ClientRepository:
    def __init__(self):
        self.clients = {}
    
    def save(self, client):
        self.clients[client.id] = client
    
    def get(self, client_id):
        if client_id not in self.clients:
            raise KeyError("Client not found")
        return self.clients[client_id]

    def list(self):
        return list(self.clients.values())
    
    def remove(self, client_id):
        if client_id not in self.clients:
            raise KeyError("Client not found")
        del self.clients[client_id]