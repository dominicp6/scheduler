from datetime import datetime


class Task(object):
    def __init__(self,
                 name: str,
                 priority: int,
                 due_date: datetime,
                 hours: float,
                 task_type: str,
                 status: str = "Not Started"):
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.hours_remaining = round(hours, 1)
        self.status = status
        self.task_type = task_type
        if self.task_type == "reading":
            self.preferred_times = {'weekday': ('afternoon',), 'weekend': ('afternoon',)}
            self.max_time_working = 1  # reading should be done in short bursts
        elif self.task_type == "writing":
            self.preferred_times = {'weekday': ('morning',), 'weekend': ('morning',)}
            self.max_time_working = 2  # writing can be done in longer bursts
        elif self.task_type == "coding":
            self.preferred_times = {'weekday': ('morning', 'afternoon'), 'weekend': ()}
            self.max_time_working = 3  # coding projects can be done for up to 3 hours at a time
        elif self.task_type == "research":
            self.preferred_times = {'weekday': ('morning',), 'weekend': ()}
            self.max_time_working = 3  # research projects can be done for up to 3 hours at a time
        elif self.task_type == "extra":
            self.preferred_times = {'weekday': ('afternoon',), 'weekend': ('morning', 'afternoon')}
            self.max_time_working = 2  # extra projects can be done for up to 2 hours at a time
        else:
            raise ValueError("Task type must be one of the following: 'reading', 'writing', 'coding', 'research', 'extra'")

    def __str__(self):
        return f"{self.name} ({self.status} - {self.hours_remaining} hours remaining, " \
               f"priority {self.priority}, due {self.due_date}, " \
               f"importance {round(self.compute_importance(datetime.now()), 2)}))"

    def work(self, hours: float, current_time: datetime, verbose: bool = False):
        self.hours_remaining = round(self.hours_remaining - hours, 1)
        if self.status == "Not Started":
            self.status = "In Progress"
        if self.hours_remaining <= 0:
            self.status = "Completed"
        if (self.due_date - current_time).days <= 0 and self.status != "Completed":
            self.status = "Overdue"

        if hours > 0 and verbose:
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
