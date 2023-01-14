from datetime import datetime

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

    def schedule_today(self):
        return self.schedule_day(datetime.today())

    def schedule_day(self, day: datetime):
        day_type = self._get_day_type(day)
        tasks = self.task_list.get_tasks_by_importance(day)
        [print(task) for task in tasks]
        available_hours = [list(timeslot) for timeslot in self.working_hours[day_type]]
        morning_hours = (available_hours[0][0], available_hours[0][1])
        afternoon_hours = (available_hours[1][0], available_hours[1][1])
        morning_hours_remaining = available_hours[0][1] - available_hours[0][0]
        afternoon_hours_remaining = available_hours[1][1] - available_hours[1][0]
        schedule = Schedule(available_hours=available_hours)
        for task in tasks:
            if task.status == "Completed":
                continue

            # Schedule morning tasks
            if morning_hours_remaining > 0:
                if (task.hours_remaining > 10 and "afternoon" not in task.preferred_times[day_type]) \
                        or ("morning" in task.preferred_times[day_type]):
                    if task.hours_remaining >= morning_hours_remaining:
                        schedule.add_task(task, (morning_hours[0], morning_hours[1]))
                        morning_hours_remaining, morning_hours = 0, None
                    elif task.hours_remaining < morning_hours_remaining:
                        schedule.add_task(task, (morning_hours[0], morning_hours[0] + task.hours_remaining))
                        morning_hours = (morning_hours[0] + task.hours_remaining, morning_hours[1])
                        morning_hours_remaining -= task.hours_remaining
                        continue
                    else:
                        continue
            # Schedule afternoon tasks
            else:
                if afternoon_hours_remaining > 0:
                    if task.hours_remaining >= afternoon_hours_remaining:
                        schedule.add_task(task, (afternoon_hours[0], afternoon_hours[1]))
                        afternoon_hours_remaining, afternoon_hours = 0, None
                    elif task.hours_remaining < afternoon_hours_remaining:
                        schedule.add_task(task, (afternoon_hours[0], afternoon_hours[0] + task.hours_remaining))
                        afternoon_hours = (afternoon_hours[0] + task.hours_remaining, afternoon_hours[1])
                        afternoon_hours_remaining -= task.hours_remaining
                        continue
                    else:
                        continue

        return schedule
