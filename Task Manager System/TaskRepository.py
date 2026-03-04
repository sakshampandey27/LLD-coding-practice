class TaskRepository:
    def __init__(self):
        self._tasks = {}
    
    def save(self, task):
        self._tasks[task.id] = task
    
    def get(self, task_id):
        if task_id not in self._tasks:
            raise KeyError("Task ID does not exist")
        return self._tasks.get(task_id)
    
    def list(self):
        return list(self._tasks.values())