import bisect

from Task import Task
from utils import get_input


class Schedule(object):
    def __init__(self, available_hours: list[list[int]]):
        self.available_hours = available_hours
        self.remaining_hours = available_hours
        self.schedule = []

    def __str__(self):
        string = "=======================================================================\n"
        for (time, task) in self.schedule:
            string += f"{task.name} at {time}\n"
        string += "=======================================================================\n"
        string += "\n"

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

    def execute(self, day, verbose=False, interactive=False):
        for (time, task) in self.schedule:
            if interactive:
                hours = get_input(f"> How many hours did you work on {task.name}? ({task.hours_remaining} remaining): ", float)
                task.work(hours, day, verbose=verbose)
            else:
                task.work(time[1]-time[0], day, verbose=verbose)
