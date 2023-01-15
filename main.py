import datetime
import os

from Task import Task
from TaskList import TaskList
from TaskScheduler import TaskScheduler
from utils import get_input, load_tasks_from_file, save_tasks_to_file


if __name__ == '__main__':
    while True:
        tasks = load_tasks_from_file("./data/tasks.txt")
        task_list = TaskList(tasks=tasks)
        print("Welcome to the Task Scheduler!")
        print("Please enter the number of the option you would like to choose:")
        print("1. Create a new task")
        print("2. Show today's schedule")
        print("3. Show all tasks")
        print("0. Execute today's schedule")
        option = input("Option: ")
        if option == "1":
            print("Creating a new task...")
            name = get_input("Name: ", str)
            priority = get_input("Priority: ", int, [1, 2, 3])
            hours = get_input("Hours: ", float)
            task_type = get_input("Task type: ", str, ["research", "reading", "coding", "extra"])
            due_date = get_input("Due date: ", datetime.datetime)
            task = Task(name=name,
                        priority=priority,
                        hours=hours,
                        task_type=task_type,
                        due_date=due_date)
            print("Task created!")
            print(task)
            task_list.add(task)
            save_tasks_to_file("./data/tasks.txt", task_list.tasks)
            input()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif option == "2":
            print("Showing today's schedule...")
            today = datetime.datetime.today()
            print(f"Schedule for {today.strftime('%A, %d %B %Y')}:")
            scheduler = TaskScheduler(task_list, working_hours={'weekday': ((9, 12), (13, 17)), 'weekend': ((10, 12), (13, 16))})
            schedule = scheduler.schedule_day(today)
            print(schedule)
            input()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif option == "3":
            print("Showing all tasks...")
            for task in task_list.tasks:
                print(task)
            input()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif option == "0":
            print("Executing today's schedule...")
            today = datetime.datetime.today()
            print(f"Schedule for {today.strftime('%A, %d %B %Y')}:")
            scheduler = TaskScheduler(task_list, working_hours={'weekday': ((9, 12), (13, 17)), 'weekend': ((10, 12), (13, 16))})
            schedule = scheduler.schedule_day(today)
            print(schedule)
            print("Executing...")
            schedule.execute(today)
            print("Done!")
            input()
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("Invalid option. Please try again.")
