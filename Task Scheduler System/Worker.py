class Worker:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def poll(self):
        task = self.scheduler.getNextTask()

        if not task:
            print("No tasks ready to execute")
            return

        print(f"Executing {task.function_name} with payload {task.payload}")

        try:
            # Simulated execution
            print("Task executed successfully")
            self.scheduler.markCompleted(task.id)

        except Exception:
            self.scheduler.markFailed(task.id)
