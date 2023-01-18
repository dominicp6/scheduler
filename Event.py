from datetime import datetime

class Event(object):
    def __init__(self, 
                 name: str, 
                 date: datetime, 
                 start_time: float, 
                 end_time: float, 
                 g_calender_event: bool):
        self.name = name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.g_calender_event = g_calender_event

    def __str__(self):
        return f"{self.name} ({self.date} {self.start_time}-{self.end_time})"