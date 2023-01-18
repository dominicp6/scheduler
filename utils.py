from datetime import datetime

from Task import Task
from Event import Event


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


def load_events_from_file(file_path: str):
    with open(file_path, "r") as file:
        events = []
        for line in file:
            event = line.split(",")
            events.append(Event(name=event[0],
                                date=datetime.strptime(event[1], "%d/%m/%Y"),
                                start_time=float(event[2]),
                                end_time=float(event[3]),
                                g_calender_event=eval(event[4])))
        return events


def save_events_to_file(file_path: str, events: list[Event]):
    with open(file_path, "w") as file:
        for event in events:
            line = f"{event.name},{event.date.strftime('%d/%m/%Y')},{event.start_time},{event.end_time},{event.g_calender_event}"
            line = line.rstrip()
            print(line, file=file)
