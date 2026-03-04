class TicketRepository:
    def __init__(self):
        self.tickets = {}
    
    def save(self, ticket):
        self.tickets[ticket.id] = ticket
    
    def get(self, ticket_id):
        if not ticket_id in self.tickets:
            raise KeyError("Ticket does not exist")
        return self.tickets[ticket_id]
    
    def list(self):
        return list(self.tickets.values())
    
    def remove(self, ticket_id):
        if not ticket_id in self.tickets:
            raise KeyError("Ticket does not exist")
        del self.tickets[ticket_id]