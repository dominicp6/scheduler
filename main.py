import datetime

from Task import Task
from TaskList import TaskList
from TaskScheduler import TaskScheduler


if __name__ == '__main__':
    # Create tasks
    task1 = Task(name="Fokker-Planck equation for Hummer Modification",
                 priority=1,
                 hours=2.5,
                 task_type="research",
                 due_date=datetime.datetime(2023, 1, 20))
    task2 = Task(name="Gabriel Reading VAMPnet Integration",
                 priority=2,
                 hours=6,
                 task_type="reading",
                 due_date=datetime.datetime(2023, 1, 27))
    task3 = Task(name="Read and understand Matthew's notes",
                 priority=3,
                 hours=4,
                 task_type="reading",
                 due_date=datetime.datetime(2023, 1, 27))
    task4 = Task(name="Read water paper",
                 priority=2,
                 hours=1,
                 task_type="reading",
                 due_date=datetime.datetime(2023, 1, 20))
    # Eventually I will make this into a habit
    task5 = Task(name="Read paper from Zotero reading list",
                 priority=3,
                 hours=12,
                 task_type="reading",
                 due_date=datetime.datetime(2023, 3, 1))
    task6 = Task(name="TICA CV enhanced sampling Alanine Dipeptide",
                 priority=1,
                 hours=8,
                 task_type="coding",
                 due_date=datetime.datetime(2023, 1, 20))
    task7 = Task(name="TICA CV enhanced sampling Chignolin",
                 priority=2,
                 hours=6,
                 task_type="coding",
                 due_date=datetime.datetime(2023, 1, 22))
    task8 = Task(name="TICA CV enhanced sampling Deca Alanine",
                 priority=3,
                 hours=5,
                 task_type="coding",
                 due_date=datetime.datetime(2023, 1, 27))
    task9 = Task(name="Periodic Table of Patterns",
                 priority=2,
                 hours=5,
                 task_type="extra",
                 due_date=datetime.datetime(2023, 2, 1))

    # Create task list
    task_list = TaskList([task1, task2, task3, task4, task5, task6, task7, task8, task9])

    # Create scheduler
    scheduler = TaskScheduler(task_list,
                              working_hours={'weekday': ((9, 12), (13, 17)), 'weekend': ((10, 12), (13, 16))})

    today = datetime.datetime.today()

    days_ahead = 7

    for i in range(days_ahead):
        day = today + datetime.timedelta(days=i)
        print("")
        print(f"Schedule for {day.strftime('%A, %d %B %Y')}:")
        schedule = scheduler.schedule_day(day)
        print(schedule)
        schedule.execute(day)
