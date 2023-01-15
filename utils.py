from datetime import datetime

from Task import Task


def get_input(prompt: str, expected_type: type, options: list = None):
    while True:
        try:
            if expected_type is datetime:
                try:
                    user_input = datetime.strptime(input(prompt), "%d/%m/%Y")
                except ValueError:
                    print("Please enter a date in the format DD/MM/YYYY")
                    continue
            else:
                user_input = expected_type(input(prompt))
            if options is not None and (user_input not in options):
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please try again.")
            if options is not None:
                print(f"Options: {options}")
    return user_input


def load_tasks_from_file(file_path: str):
    with open(file_path, "r") as file:
        tasks = []
        for line in file:
            task = line.split(",")
            tasks.append(Task(name=task[0],
                              priority=int(task[1]),
                              hours=float(task[2]),
                              due_date=datetime.strptime(task[3], "%d/%m/%Y"),
                              task_type=task[4],
                              status=task[5]))
        return tasks


def save_tasks_to_file(file_path: str, tasks: list[Task]):
    tasks = [task for task in tasks if task.status != "Completed"]
    with open(file_path, "w") as file:
        for task in tasks:
            line = f"{task.name},{task.priority},{task.hours_remaining},{task.due_date.strftime('%d/%m/%Y')},{task.task_type},{task.status}"
            line = line.rstrip()
            print(line, file=file)
