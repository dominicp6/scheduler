import bisect
from datetime import datetime

from Task import Task
from Event import Event
from utils import get_input, bcolors


class Schedule(object):
    def __init__(self, date: datetime, available_hours: list[list[int]]):
        self.date = date
        self.available_hours = available_hours
        self.remaining_hours = available_hours
        self.schedule = []

    def __str__(self):
        dividing_bar = False
        string = "=======================================================================\n"
        for (time, obligation) in self.schedule:
            if time[0] > 12 and not dividing_bar:
                string += "-----------------------------------------------------------------------\n"
                dividing_bar = True
            
            if isinstance(obligation, Task):
                string = self._add_task_string(obligation, time, string)
            elif isinstance(obligation, Event):
                string = self._add_event_string(obligation, time, string)
            else:
                raise TypeError("Obligation must be a Task or Event")
                
        string += "=======================================================================\n"
        string += "\n"

        return string

    def _add_task_string(self, task: Task, time: tuple[float, float], string: str):
        days_remaining = (task.due_date - self.date).days + 1
        if days_remaining < 0:
            string += f"{task.name} at {time} {bcolors.RED}[Overdue]{bcolors.ENDC}\n"
        elif days_remaining <=2:
            if days_remaining == 0:
                string += f"{task.name} at {time} {bcolors.YELLOW}[Due Today]{bcolors.ENDC}\n"
            elif days_remaining == 1:
                string += f"{task.name} at {time} {bcolors.YELLOW}[Due Tomorrow]{bcolors.ENDC}\n"
            elif days_remaining == 2:
                string += f"{task.name} at {time} {bcolors.YELLOW}[Due {task.due_date.strftime('%A')}]{bcolors.ENDC}\n"
        else:
            string += f"{task.name} at {time}\n"

        return string

    def _add_event_string(self, event: Event, time: tuple[float, float], string: str):
        string += f"{bcolors.GREEN}{event.name} at {time}{bcolors.GREEN}\n"

        return string

    def is_available(self, time: tuple[float, float]):
        for timeslot in self.remaining_hours:
            if time[0] >= timeslot[0] and time[1] <= timeslot[1]:
                return True

        return False

    def update_remaining_hours(self, time: tuple[float, float]):
        for idx, timeslot in enumerate(self.remaining_hours):
            if time[0] == timeslot[0] and time[1] == timeslot[1]:
                del self.remaining_hours[idx]
                break
            elif time[0] == timeslot[0] and time[1] < timeslot[1]:
                self.remaining_hours[idx] = [time[1], timeslot[1]]
                break
            elif time[0] > timeslot[0] and time[1] == timeslot[1]:
                self.remaining_hours[idx] = [timeslot[0], time[0]]
                break
            elif time[0] > timeslot[0] and time[1] < timeslot[1]:
                self.remaining_hours[idx] = [timeslot[0], time[0]]
                self.remaining_hours.insert(idx+1, [time[1], timeslot[1]])
                break

    def add_task(self, task: Task, time: tuple[float, float]):
        if self.is_available(time):
            self.update_remaining_hours(time)
            bisect.insort(self.schedule, (time, task))

    def add_event(self, event: Event, time: tuple[float, float]):
        if self.is_available(time):
            print(f"Adding {event.name} at {time} on {self.date.strftime('%A, %B %d, %Y')}")
            self.update_remaining_hours(time)
            bisect.insort(self.schedule, (time, event))

    def execute(self, day, verbose=False, interactive=False):
        for (time, task) in self.schedule:
            if interactive:
                hours = get_input(f"> How many hours did you work on {task.name}? ({task.hours_remaining} remaining): ", float)
                task.work(hours, day, verbose=verbose)
            else:
                task.work(time[1]-time[0], day, verbose=verbose)
