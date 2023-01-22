from TaskList import TaskList
from Task import Task
from utils import get_input, save_tasks_to_file


class TaskManager:
    def __init__(self, task_list: TaskList):
        self.task_list = task_list
        self.selected_task_id = None
        print("Managing tasks...")
        self._show_all_tasks()
        while True:
            task = self._select_task()
            # If the user wants to quit, break
            if task is None:
                break
            else:
                self.prompt(task)

    def _show_all_tasks(self):
        for id, task in enumerate(self.task_list.tasks):
            print(f"[{id}]",task)

    def _select_task(self):
        while True:
            task_id = get_input("Which task would you like to manage?> ", int, allow_quit=True)
            # If the user wants to quit, return None
            if task_id is None:
                return None
            if task_id in range(len(self.task_list.tasks)):
                task = self.task_list.get(task_id)
                self.selected_task_id = task_id
                break
            else:
                print("Invalid task id, please try again!")

        return task

    def _init_message(self, task: Task):
        print("Managing task:", task.name)
        print("[w] Work on task")
        print("[h] Change hours remaining")
        print("[m] Move due date")
        print("[p] Change priority")
        print("[t] Change task type")
        print("[r] Rename task")
        print("[d] Delete task")
        print("[q] Quit")

    def prompt(self, task: Task):
        self._init_message(task)
        while True:
            command = get_input("What would you like to do?> ", str)
            if command == "w":
                hours = get_input("How many hours would you like to work?> ", float)
                task.work(hours)
            elif command == "h":
                remaining_hours = get_input("How many hours remaining?> ", float)
                task.change_hours_remaining(remaining_hours)
            elif command == "m":
                due_date = get_input("What is the new due date?> ", str)
                task.change_due_date(due_date)
            elif command == "p":
                priority = get_input("What is the new priority?> ", int, options=[1,2,3])
                task.change_priority(priority)
            elif command == "t":
                task_type = get_input("What is the new task type?> ", str)
                task.change_task_type(task_type)
            elif command == "r":
                name = get_input("What is the new name?> ", str)
                task.rename(name)
            elif command == "d":
                yn = get_input("Are you sure you want to delete this task?> ", str, options=["y", "n"])
                if yn == "y":
                    del self.task_list[self.selected_task_id]
                    break
            elif command == "q":
                break
            else:
                print("Invalid command, please try again!")

            save_tasks_to_file("./data/tasks.txt", self.task_list.tasks)
