import Task
import uuid
import sys

class TaskManager:
    def __init__(self):
        self.tasks = {}
    
    def generate_task_uuid(self):
        return str(uuid.uuid4())

    def create_task(self, title, description=None):
        try:
            task_id = self.generate_task_uuid()        
            self.tasks[task_id] = Task.Task(task_id, title, description)
            return task_id
        except ValueError as err:
            print(err)
            raise
    
    def assign_task(self, task_id, user_id):
        try:
            task = self.tasks[task_id]
            task.assign_user(user_id)
        except KeyError:
            print("Task ID does not exist")
            raise 
        except ValueError as err:
            print(err)
            raise

    def update_status(self, task_id, new_status):
        try:
            task = self.tasks[task_id]
            task.update_status(new_status.strip().upper())
        except KeyError:
            print("Task ID does not exist")
            raise
        except ValueError as err:
            print(err)
            raise

    def get_task(self, task_id):
        try:
            task = self.tasks[task_id]
            return task.get_summary()
        except KeyError:
            print("Task ID does not exist")
            raise

    def list_tasks(self, filter_by_status=None, filter_by_user=None):
        tasks = self.tasks.values()
        if filter_by_status:
            tasks = self.filter_tasks_by_status(tasks, filter_by_status)
        if filter_by_user:
            tasks = self.filter_tasks_by_user(tasks, filter_by_user)
        
        return [task.id for task in tasks]

    def filter_tasks_by_status(self, task_list, status):
        result_list = []
        for task in task_list:
            if task.get_status() == Task.Status[status.strip().upper()]:
                result_list.append(task)
        return result_list

    def filter_tasks_by_user(self, task_list, user):
        result_list = []
        for task in task_list:
            if task.get_assigned_user() == user:
                result_list.append(task)
        return result_list

if __name__ == "__main__":
    task_manager = TaskManager()
    task1 = task_manager.create_task(title="Task title 1", description="This is task 1")
    task2 = task_manager.create_task(title="Task title 2", description="This is task 2")
    task3 = task_manager.create_task(title="Task title 3", description="This is task 3")
    print("After Creation\n")
    print(task_manager.get_task(task1))
    print(task_manager.get_task(task2))
    print(task_manager.get_task(task3))
    task_manager.assign_task(task1, "saksham")
    task_manager.assign_task(task2, "pandey")
    print("After Assignment\n")
    print(task_manager.get_task(task1))
    print(task_manager.get_task(task2))
    task_manager.update_status(task1, "INPROGRESS")
    task_manager.update_status(task2, "COMPLETED")
    print("After Status update\n")
    print(task_manager.get_task(task1))
    print(task_manager.get_task(task2))
    print("Filtering tasks")
    print(task_manager.list_tasks())
    print(task_manager.list_tasks(filter_by_status="Inprogress"))
    print(task_manager.list_tasks(filter_by_status="Todo"))
    print(task_manager.list_tasks(filter_by_user="pandey"))
    print(task_manager.list_tasks(filter_by_status="Inprogress", filter_by_user="pandey"))
    print(task_manager.list_tasks(filter_by_status="Completed", filter_by_user="pandey"))