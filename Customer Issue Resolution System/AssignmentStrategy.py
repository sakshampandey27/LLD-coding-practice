from abc import ABC, abstractmethod

class AssignmentStrategy(ABC):
    @abstractmethod
    def assign(self):
        pass

class LeastLoadedAgentStrategy(AssignmentStrategy):
    def assign(self, agents):
        try:
            min_issues = float('inf')
            assigned_agent = None
            for agent in agents:
                active_count = agent.get_active_issues_count()
                if active_count < min_issues:
                    min_issues = active_count
                    assigned_agent = agent
            return assigned_agent
        except Exception as err:
            raise 