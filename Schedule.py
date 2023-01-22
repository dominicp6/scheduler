import bisect
from datetime import datetime

from Task import Task
from Event import Event
from utils import get_input, bcolors


class Schedule(object):
    def __init__(self, date: datetime, available_hours: list[list[int]], events: list[Event] = None):
        self.date = date
        self.available_hours = available_hours
        self.remaining_hours = available_hours
        self.schedule = []
        if events is not None:
            # Add the events (this updates the remaining hours as well as the schedule)
            [self.add_event(event) for event in events]

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
        string += f"{bcolors.GREEN}{event.name} at {time}{bcolors.ENDC}\n"

        return string

    def is_available(self, time: tuple[float, float]):
        # Only interested in times between 9am and 5pm
        # TODO: change this so that it is not hard coded
        time = list(time)
        if time[0] <= 9 and time[1] <= 9:
            return True
        elif time[0] >= 17 and time[1] >= 17:
            return True
        elif time[0] <= 9 and time[1] >= 9:
            time[0] = 9
        elif time[0] <= 17 and time[1] >= 17:
            time[1] = 17
        else:
            pass

        for timeslot in self.remaining_hours:
            if time[0] >= timeslot[0] and time[1] <= timeslot[1]:
                return True

        return False

    def update_remaining_hours(self, time: tuple[float, float]):
        # TODO: change this so that it is not hard coded and also refactor it
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
            # NB: Only events will possibly be scheduled outside of the working day
            elif timeslot[0] == 9:
                # This is the first timeslot of the day
                if time[0] < timeslot[0] and time[1] < timeslot[1]:
                    self.remaining_hours[idx] = [time[1], timeslot[1]]
                    break
                elif time[0] < timeslot[0] and time[1] == timeslot[1]:
                    del self.remaining_hours[idx]
                    break
                elif time[0] < timeslot[0] and time[1] < timeslot[0]:
                    break
                else:
                    continue
            elif timeslot[1] == 17:
                # This is the last timeslot of the day
                if time[0] > timeslot[0] and time[1] > timeslot[1]:
                    self.remaining_hours[idx] = [timeslot[0], time[0]]
                    break
                elif time[0] == timeslot[0] and time[1] > timeslot[1]:
                    del self.remaining_hours[idx]
                    break
                elif time[0] > timeslot[1] and time[1] > timeslot[1]:
                    break
                else:
                    continue
            else:
                continue

    def add_task(self, task: Task, time: tuple[float, float]):
        if self.is_available(time):
            self.update_remaining_hours(time)
            bisect.insort(self.schedule, (time, task))

    def add_event(self, event: Event):
        time = (event.start_time, event.end_time)
        assert self.is_available(time), f"Your schedule is already booked for the time of this event. {event.name} at {time} on {self.date.strftime('%A, %B %d, %Y')}. Make sure you add events to your schedule before adding tasks. Heres your schedule:\n{self}"
        self.update_remaining_hours(time)
        bisect.insort(self.schedule, (time, event))

    def execute(self, day, verbose=False, interactive=False):
        for (time, obligation) in self.schedule:
            if isinstance(obligation, Event):
                continue
            elif isinstance(obligation, Task):
                if interactive:
                    hours = get_input(f"> How many hours did you work on {obligation.name}? ({obligation.hours_remaining} remaining): ", float)
                    obligation.work(hours, day, verbose=verbose)
                else:
                    obligation.work(time[1]-time[0], day, verbose=verbose)
            else:
                raise TypeError("Obligation must be a Task or Event")
