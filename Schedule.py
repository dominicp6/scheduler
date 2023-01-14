from Task import Task


class Schedule(object):
    def __init__(self, available_hours: list[list[int]]):
        self.available_hours = available_hours
        self.remaining_hours = available_hours
        self.schedule = []

    def __str__(self):
        string = "=======================================================================\n"
        for (task, time) in self.schedule:
            string += f"{task.name} at {time}\n"
        string += "=======================================================================\n"
        string += "\n"

        return string

    def is_available(self, time: tuple[int, int]):
        for timeslot in self.remaining_hours:
            if time[0] >= timeslot[0] and time[1] <= timeslot[1]:
                return True

        return False

    def update_remaining_hours(self, time: tuple[int, int]):
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

    def add_task(self, task: Task, time: tuple[int, int]):
        if self.is_available(time):
            self.update_remaining_hours(time)
            self.schedule.append((task, time))

    def execute(self, day):
        for (task, time) in self.schedule:
            task.work(time[1]-time[0], day)
