from datetime import datetime

from Task import Task


class TaskList(object):
    def __init__(self, tasks: list[Task] = None):
        if tasks is None:
            tasks = []
        self.tasks = tasks

    def __str__(self):
        for task in self.tasks:
            print(task)

    def get(self, id: int):
        return self.tasks[id]

    def add(self, task: Task):
        self.tasks.append(task)

    def get_tasks_by_priority(self, priority: int):
        return [task for task in self.tasks if task.priority == priority]

    def get_tasks_by_status(self, status: str):
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_date(self, date):
        return [task for task in self.tasks if task.due_date == date]

    def get_tasks_by_name(self, name):
        return [task for task in self.tasks if task.name == name]

    def get_tasks_by_importance(self, current_time: datetime):
        return sorted(self.tasks, key=lambda task: task.compute_importance(current_time), reverse=True)
