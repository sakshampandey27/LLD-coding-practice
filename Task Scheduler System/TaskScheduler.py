import heapq
from datetime import datetime, timedelta
import time
from Worker import Worker
from Task import Task, TaskStatus

class TaskScheduler:
    def __init__(self):
        self.task_queue = []
        self.task_map = {}

    def submitTask(self, function_name, payload, scheduled_time, priority):
        task = Task(function_name, payload, scheduled_time, priority)
        heap_item = (task.scheduled_time, task.priority, task.created_time, task)
        heapq.heappush(self.task_queue, heap_item)
        self.task_map[task.id] = task
        return task.id

    def getNextTask(self):
        if not self.task_queue:
            return None

        heap_item = self.task_queue[0]
        task = heap_item[3]
        if task.scheduled_time > datetime.now():
            return None

        heapq.heappop(self.task_queue)
        task.set_running()
        return task

    def markCompleted(self, task_id):
        task = self.task_map.get(task_id)
        if task:
            task.mark_completed()

    def markFailed(self, task_id):
        task = self.task_map.get(task_id)
        if task:
            task.mark_completed()


if __name__ == "__main__":
    scheduler = TaskScheduler()
    now = datetime.now()

    t1 = scheduler.submitTask(
        "sendEmail",
        {"userId": 101},
        now,
        priority=1
    )

    t2 = scheduler.submitTask(
        "generateReport",
        {"reportId": 55},
        now + timedelta(seconds=5),
        priority=2
    )

    worker = Worker(scheduler)
    worker.poll()
    time.sleep(5)
    worker.poll()