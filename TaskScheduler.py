from datetime import datetime, timedelta
from copy import deepcopy

from Task import Task
from TaskList import TaskList
from EventList import EventList
from Schedule import Schedule


class TaskScheduler(object):
    def __init__(self, task_list: TaskList, event_list: EventList, working_hours):
        self.task_list = task_list
        self.event_list = event_list
        self.working_hours = working_hours if working_hours else {'weekday': ((9, 12), (13, 17)),
                                                                  'weekend': ((10, 12), (13, 16))}

    def _get_day_type(self, day: datetime):
        if day.weekday() < 5:
            day = 'weekday'
        else:
            day = 'weekend'

        return day

    def _hours_remaining(self, timeslots: list[list[float, float]]):
        hours_remaining = 0
        for timeslot in timeslots:
            if timeslot is None:
                continue
            else:
                hours_remaining += timeslot[1] - timeslot[0]

        return hours_remaining

    def _classify_timeslots(self, available_hours: list[list[float, float]]):
        morning_hours = []
        afternoon_hours = []
        for timeslot in available_hours:
            if timeslot[0] < self.working_hours['weekday'][0][1]:
                morning_hours.append(timeslot)
            else:
                afternoon_hours.append(timeslot)

        return morning_hours, afternoon_hours

    def _adjust_first_timeslot(self, timeslots, adjusted_timeslot):
        if adjusted_timeslot is None:
            timeslots.pop(0)
        else:
            timeslots[0] = adjusted_timeslot

        return timeslots

    def get_available_timeslots(self, day: datetime):
        day_type = self._get_day_type(day)
        available_hours = [list(timeslot) for timeslot in self.working_hours[day_type]]
        events = self.event_list.get_events_by_day(day)

        # Adjust available hours based on events
        for event in events:
            event_start = event.start_time
            event_end = event.end_time
            for i, timeslot in enumerate(available_hours):
                if event_start <= timeslot[0] < event_end:
                    available_hours[i][0] = event_end
                elif event_start < timeslot[1] <= event_end:
                    available_hours[i][1] = event_start
                elif timeslot[0] <= event_start and event_end <= timeslot[1]:
                    available_hours[i] = [timeslot[0], event_start]
                    available_hours.append([event_end, timeslot[1]])

        return available_hours

    def schedule_task(self,
                      task: Task,
                      schedule: Schedule,
                      timeslot: list[float, float]):

        assert timeslot is not None 
        assert timeslot[0] < timeslot[1]
        timeslot_hours_remaining = timeslot[1] - timeslot[0]

        if task.hours_remaining >= timeslot_hours_remaining:
            if task.max_time_working >= timeslot_hours_remaining:
                # Schedule task for the remaining time in the timeslot
                schedule.add_task(task, (timeslot[0], timeslot[1]))
                timeslot = None
            else:
                # Schedule task for the max time working
                schedule.add_task(task, (timeslot[0], timeslot[0] + task.max_time_working))
                timeslot = (timeslot[0] + task.max_time_working, timeslot[1])
        else:
            if task.hours_remaining >= task.max_time_working:
                # Schedule task for the max time working
                schedule.add_task(task, (timeslot[0], timeslot[0] + task.max_time_working))
                timeslot = (timeslot[0] + task.max_time_working, timeslot[1])
            else:
                # Schedule task for the remaining hours
                schedule.add_task(task, (timeslot[0], timeslot[0] + task.hours_remaining))
                timeslot = (timeslot[0] + task.hours_remaining, timeslot[1])

        return timeslot

    def schedule_today(self):
        return self.schedule_day(datetime.today())

    def schedule_week(self):
        # Create a copy of the task list
        task_list = deepcopy(self.task_list)

        # Create a schedule for each day of the week
        schedules = {}
        for day in range(7):
            date = datetime.today() + timedelta(days=day)
            schedules[date] = self.schedule_day(date)
            # Execute the tasks in the schedule
            schedules[date].execute(date)

        # Restore the task list
        self.task_list = task_list

        return schedules

    def schedule_day(self, day: datetime):
        day_type = self._get_day_type(day)
        tasks = self.task_list.get_tasks_by_importance(day)
        available_hours = self.get_available_timeslots(day)
        morning_hours, afternoon_hours = self._classify_timeslots(available_hours)
        schedule = Schedule(available_hours=available_hours)
        # TODO: Deal with edge cases e.g. after the loop there are still available hours and available tasks
        for task in tasks:
            if task.status == "Completed":
                continue

            # Schedule morning tasks
            if self._hours_remaining(morning_hours) > 0 and "morning" in task.preferred_times[day_type]:
                adjusted_timeslot = self.schedule_task(task, schedule, morning_hours[0])
                morning_hours = self._adjust_first_timeslot(morning_hours, adjusted_timeslot)
                continue
            # Schedule afternoon tasks
            else:
                if self._hours_remaining(afternoon_hours) > 0 and "afternoon" in task.preferred_times[day_type]:
                    adjusted_timeslot = self.schedule_task(task, schedule, afternoon_hours[0])
                    afternoon_hours = self._adjust_first_timeslot(afternoon_hours, adjusted_timeslot)
                    continue

            # Break if no more hours available
            if self._hours_remaining(morning_hours) == 0 and self._hours_remaining(afternoon_hours) == 0:
                break

        return schedule
