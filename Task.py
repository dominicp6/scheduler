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
        self.preferred_times = self._get_preferred_times(task_type)
        self.max_time_working = self._get_max_time_working(task_type)
        
    @staticmethod
    def _get_preferred_times(task_type: str):
        if task_type == "reading":
            preferred_times = {'weekday': ('afternoon',), 'weekend': ('afternoon',)}
        elif task_type == "writing":
            preferred_times = {'weekday': ('morning',), 'weekend': ('morning',)}
        elif task_type == "coding":
            preferred_times = {'weekday': ('morning', 'afternoon'), 'weekend': ('morning')}
        elif task_type == "research":
            preferred_times = {'weekday': ('morning',), 'weekend': ()}
        elif task_type == "admin":
            preferred_times = {'weekday': ('morning','afternoon'), 'weekend': ('morning', 'afternoon')}
        elif task_type == "extra":
            preferred_times = {'weekday': ('afternoon',), 'weekend': ('morning', 'afternoon')}
        else:
            raise ValueError("Task type must be one of the following: 'reading', 'writing', 'coding', 'research', 'admin', 'extra'")

        return preferred_times

    @staticmethod
    def _get_max_time_working(task_type: str):
        if task_type == "reading":
            # reading should be done in short bursts
            max_time_working = 1
        elif task_type == "writing":
            # writing can be done in longer bursts
            max_time_working = 2
        elif task_type == "coding":
            # coding projects can be done for up to 3 hours at a time
            max_time_working = 3
        elif task_type == "research":
            # research projects can be done for up to 3 hours at a time
            max_time_working = 3
        elif task_type == "admin":
            # admin tasks can be done in short bursts
            max_time_working = 1
        elif task_type == "extra":
            # extra projects can be done for up to 2 hours at a time
            max_time_working = 2
        else:
            raise ValueError("Task type must be one of the following: 'reading', 'writing', 'coding', 'research', 'admin', 'extra'")

        return max_time_working

    def __str__(self):
        return f"{self.name} ({self.status.rstrip()} - {self.hours_remaining} hours remaining, " \
               f"priority {self.priority}, due {self.due_date}, " \
               f"importance {round(self.compute_importance(datetime.now()), 2)}))"

    def work(self, hours: float, current_time: datetime, verbose: bool = False):
        self.hours_remaining = round(self.hours_remaining - hours, 1)
        self.compute_task_status(current_time, hours)

        if hours > 0 and verbose:
            if (self.due_date - current_time).days <= 3:
                due_in = (self.due_date - current_time).days
                print(f"{self.name} worked on for {hours} hours. {self.hours_remaining} hours remaining. "
                      f"[Due in {due_in} days]")
            else:
                print(f"{self.name} worked on for {hours} hours. {self.hours_remaining} hours remaining.")

    def compute_task_status(self, current_time: datetime, hours_worked: float = 0):
        days_remaining = (self.due_date - current_time).days + 2
        if days_remaining >=1:
            if self.status.rstrip() == "Not Started" and hours_worked == 0:
                self.status = "Not Started"
            elif self.hours_remaining > 0:
                self.status = "In Progress"
            else:
                self.status = "Completed"
        else:
            if self.hours_remaining > 0:
                self.status = "Overdue"
            else:
                self.status = "Completed"

    def compute_importance(self, current_time: datetime):
        self.compute_task_status(current_time)
        if self.status == "Completed":
            return 0
        elif self.status == "Overdue":
            return self._compute_overdue_importance(current_time)
        elif self.status == "Not Started" or "In Progress":
            return self._compute_in_progress_importance(current_time)

    def _compute_overdue_importance(self, current_time: datetime):
        # Depends on the task priority and how many days overdue it is
        days_overdue = (current_time - self.due_date).days - 1
        if self.priority == 1:
            return (self.hours_remaining/self.priority) * (1 + days_overdue**3 / self.priority)
        elif self.priority == 2:
            return (self.hours_remaining/self.priority) * (1 + days_overdue**2 / self.priority)
        elif self.priority == 3:
            return (self.hours_remaining/self.priority) * (1 + days_overdue / self.priority)
        else:
            raise ValueError("Priority must be an integer between 1 and 3.")

    def _compute_in_progress_importance(self, current_time: datetime):
        days_remaining = (self.due_date - current_time).days + 2 # +2 to avoid division by zero; days_remaining=1 means due today.
        return 1/self.priority * self.hours_remaining/days_remaining
            

    def change_priority(self, new_priority: int):
        print(f"Changing priority of {self.name} from {self.priority} to {new_priority}.")
        self.priority = new_priority

    def change_due_date(self, new_due_date: str):
        print(f"Changing due date of {self.name} from {self.due_date} to {new_due_date}.")
        try:
            self.due_date = datetime.strptime(new_due_date, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format, please use dd/mm/yyyy. Date not changed.")
    
    def change_hours_remaining(self, new_hours_remaining: float):
        print(f"Changing hours remaining of {self.name} from {self.hours_remaining} to {new_hours_remaining}.")
        self.hours_remaining = new_hours_remaining

    def change_status(self, new_status: str):
        print(f"Changing status of {self.name} from {self.status} to {new_status}.")
        self.status = new_status
        if self.status == "Completed":
            print(f"Task {self.name} completed, setting hours remaining to 0.")
            self.hours_remaining = 0

    def change_task_type(self, new_task_type: str):
        print(f"Changing task type of {self.name} from {self.task_type} to {new_task_type}.")
        self.task_type = new_task_type
        self.preferred_times = self._get_preferred_times(new_task_type)
        self.max_time_working = self._get_max_time_working(new_task_type)

    def rename(self, new_name: str):
        print(f"Changing name of {self.name} to {new_name}.")
        self.name = new_name
