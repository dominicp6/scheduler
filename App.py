import os
import json
from datetime import datetime, timedelta
from copy import deepcopy

import pytz

from Task import Task
from Event import Event
from TaskList import TaskList
from EventList import EventList
from TaskScheduler import TaskScheduler
from utils import get_input, load_tasks_from_file, save_tasks_to_file, load_events_from_file, save_events_to_file


class App:

    def __init__(self):
        tasks = load_tasks_from_file("./data/tasks.txt")
        events = load_events_from_file("./data/events.txt")
        self.task_list = TaskList(tasks=tasks)
        self.event_list = EventList(events=events)
        self.today = datetime.today()
        self.working_hours = {'weekday': ((9, 12), (13, 17)), 'weekend': ((10, 12), (13, 16))}
        self.prompt()

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def finish(self):
        input()
        self.clear()
    
    def _init_message(self):
        print("Welcome to the Task Scheduler! [alpha v1.0]")
        print("[n] Create new task")
        print("[t] Show today's schedule")
        print("[w] Show week's schedule")
        print("[a] Show all tasks")
        print("[e] Execute today's schedule")
        print("[0] Execute single task")
        print("[s] Sync with Google Calendar")
        print("[q] Quit")

    def prompt(self):
        while True:
            self._init_message()
            option = input("> ")
            if option == "n":
                self.create_new_task()
            elif option == "t":
                self.show_todays_schedule()
            elif option == "w":
                self.show_weeks_schedule()
            elif option == "a":
                self.show_all_tasks()
            elif option == "e":
                self.execute_todays_schedule()
            elif option == "0":
                self.execute_single_task()
            elif option == "s":
                self.sync_with_google_calendar()
            elif option == "q":
                exit()
            else:
                print("Invalid option, please try again!")

    def create_new_task(self):
        print("Creating a new task...")
        name = get_input("Name: ", str)
        priority = get_input("Priority: ", int, [1, 2, 3])
        task_type = get_input("Task type: ", str, ["research", "reading", "coding", "writing", "extra"])
        due_date = get_input("Due date: ", datetime)
        hours = get_input("Hours: ", float)
        task = Task(name=name,
                    priority=priority,
                    hours=hours,
                    task_type=task_type,
                    due_date=due_date)
        print("Task created!")
        print(task)
        self.task_list.add(task)
        save_tasks_to_file("./data/tasks.txt", self.task_list.tasks)
        self.finish()

    def show_todays_schedule(self):
        print("Showing today's schedule...")
        print(f"Schedule for {self.today.strftime('%A, %d %B %Y')}:")
        scheduler = TaskScheduler(self.task_list, self.event_list, working_hours=self.working_hours)
        schedule = scheduler.schedule_day(self.today)
        print(schedule)
        self.finish()

    def show_weeks_schedule(self):
        print("Showing this week's schedule...")
        scheduler = TaskScheduler(deepcopy(self.task_list), self.event_list, working_hours=self.working_hours)
        schedules = scheduler.schedule_week()
        for date, schedule in schedules.items():
            print(f"Schedule for {date.strftime('%A, %d %B %Y')}:")
            print(schedule)
        self.finish()

    def show_all_tasks(self):
        print("Showing all tasks...")
        for id, task in enumerate(self.task_list.tasks):
            print(f"[{id}]",task)
        self.finish()

    def execute_todays_schedule(self):
        print("Executing today's schedule...")
        print(f"Schedule for {self.today.strftime('%A, %d %B %Y')}:")
        scheduler = TaskScheduler(self.task_list, self.event_list, working_hours=self.working_hours)
        schedule = scheduler.schedule_day(self.today)
        print(schedule)
        print("Executing...")
        schedule.execute(self.today, interactive=True, verbose=True)
        save_tasks_to_file("./data/tasks.txt", self.task_list.tasks)
        print("Done!")
        self.finish()

    def execute_single_task(self):
        print("Executing a single task...")
        task_id = get_input("Task ID: ", int)
        task = self.task_list.get(task_id)
        print("Executing...")
        hours = get_input(f"> How many hours did you work on {task.name}? ({task.hours_remaining} remaining): ", float)
        task.work(hours, self.today, verbose=True)
        save_tasks_to_file("./data/tasks.txt", self.task_list.tasks)
        print("Done!")
        self.finish()

    def sync_with_google_calendar(self):
        print("Syncing with Google Calendar...")
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build

        with open('/home/dominic/PycharmProjects/scheduler/auth/client_secret.json') as file:
            creds_data = json.load(file)

        # Create an OAuth2 flow
        flow = InstalledAppFlow.from_client_config(
            client_config=creds_data,
            scopes=['https://www.googleapis.com/auth/calendar']
        )

        # Run the flow to obtain the refresh token
        flow.run_local_server()

        # Save the refresh token to a file
        creds = flow.credentials
        with open('path/to/token.json', 'w') as f:
            f.write(creds.to_json())

        # Use the application default credentials
        creds = Credentials.from_authorized_user_file('/home/dominic/PycharmProjects/scheduler/auth/token.json')
        service = build('calendar', 'v3', credentials=creds)

        # Get the events for the next week
        timezone = pytz.timezone("Europe/London")
        now = datetime.now(timezone).isoformat() 
        end_of_week = (datetime.now() + timedelta(days=7)).isoformat() 
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              timeMax=end_of_week, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        # Create an EventList object and add the events to it
        self.event_list = EventList()
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
            end = datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date')))
            self.event_list.add_event(Event(event['summary'], start, end))

        self.finish()
