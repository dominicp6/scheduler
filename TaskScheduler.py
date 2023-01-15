from datetime import datetime, timedelta
from copy import deepcopy

from Task import Task
from TaskList import TaskList
from Schedule import Schedule


class TaskScheduler(object):
    def __init__(self, task_list: TaskList, working_hours):
        self.task_list = task_list
        self.working_hours = working_hours if working_hours else {'weekday': ((9, 12), (13, 17)),
                                                                  'weekend': ((10, 12), (13, 16))}

    def _get_day_type(self, day: datetime):
        if day.weekday() < 5:
            day = 'weekday'
        else:
            day = 'weekend'

        return day

    def _hours_remaining(self, timeslot: tuple[float, float]):
        if timeslot is None:
            return 0
        return timeslot[1] - timeslot[0]

    def schedule_task(self,
                      task: Task,
                      schedule: Schedule,
                      timeslot: tuple[float, float]):

        assert timeslot is not None
        timeslot_hours_remaining = timeslot[1] - timeslot[0]
        assert timeslot_hours_remaining > 0

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
        available_hours = [list(timeslot) for timeslot in self.working_hours[day_type]]
        morning_hours = (available_hours[0][0], available_hours[0][1])
        afternoon_hours = (available_hours[1][0], available_hours[1][1])
        schedule = Schedule(available_hours=available_hours)
        for task in tasks:
            if task.status == "Completed":
                continue

            # Schedule morning tasks
            if self._hours_remaining(morning_hours) > 0 and "morning" in task.preferred_times[day_type]:
                morning_hours = self.schedule_task(task, schedule, morning_hours)
                continue
            # Schedule afternoon tasks
            else:
                if self._hours_remaining(afternoon_hours) > 0 and "afternoon" in task.preferred_times[day_type]:
                    afternoon_hours = self.schedule_task(task, schedule, afternoon_hours)
                    continue

            # Break if no more hours available
            if self._hours_remaining(morning_hours) == 0 and self._hours_remaining(afternoon_hours) == 0:
                break

        return schedule
