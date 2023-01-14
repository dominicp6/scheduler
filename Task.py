from datetime import datetime


class Task(object):
    def __init__(self,
                 name: str,
                 priority: int,
                 due_date: datetime,
                 hours: float,
                 task_type: str = None,
                 preferred_times: dict[str, tuple[set[str]]] = None):
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.hours_remaining = hours
        self.status = "Not Started"
        self.task_type = task_type
        if self.task_type is not None and preferred_times is None:
            if self.task_type == "reading":
                self.preferred_times = {'weekday': ('afternoon',), 'weekend': ('afternoon',)}
            elif self.task_type == "writing":
                self.preferred_times = {'weekday': ('morning',), 'weekend': ('morning',)}
            elif self.task_type == "coding":
                self.preferred_times = {'weekday': ('morning', 'afternoon'), 'weekend': ()}
            elif self.task_type == "research":
                self.preferred_times = {'weekday': ('morning',), 'weekend': ()}
            elif self.task_type == "extra":
                self.preferred_times = {'weekday': ('afternoon',), 'weekend': ('morning', 'afternoon')}
        else:
            self.preferred_times = preferred_times if preferred_times else {'weekday': ('morning', 'afternoon'),
                                                                            'weekend': ('morning', 'afternoon')}

    def __str__(self):
        return f"{self.name} ({self.status} - {self.hours_remaining} hours remaining, " \
               f"priority {self.priority}, due {self.due_date}, " \
               f"importance {round(self.compute_importance(datetime.now()), 2)}))"

    def work(self, hours: float, current_time: datetime):
        self.hours_remaining -= hours
        if self.status == "Not Started":
            self.status = "In Progress"
        if self.hours_remaining <= 0:
            self.status = "Completed"
        if (self.due_date - current_time).days <= 0:
            self.status = "Overdue"

        if hours > 0:
            if (self.due_date - current_time).days <= 3:
                due_in = (self.due_date - current_time).days
                print(f"{self.name} worked on for {hours} hours. {self.hours_remaining} hours remaining. "
                      f"[Due in {due_in} days]")
            else:
                print(f"{self.name} worked on for {hours} hours. {self.hours_remaining} hours remaining.")

    def compute_importance(self, current_time: datetime):
        if self.status == "Completed":
            return 0
        elif self.status == "Overdue":
            return float("inf")
        else:
            try:
                return 1/self.priority * self.hours_remaining/(self.due_date - current_time).days
            except ZeroDivisionError:
                return float("inf")