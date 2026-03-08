class AgentRepository:
    def __init__(self):
        self.agents = {}
    
    def save(self, agent):
        self.agents[agent.id] = agent
    
    def get(self, agent_id):
        if agent_id not in self.agents:
            raise KeyError("Agent not found")
        return self.agents[agent_id]
    
    def list(self):
        return sorted(list(self.agents.values()), key=lambda item: item.id)