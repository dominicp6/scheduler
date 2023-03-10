from datetime import datetime

from Event import Event


class EventList(object):
    def __init__(self, events: list[Event] = None):
        if events is None:
            events = []
        self.events = events

    def __str__(self):
        for event in self.events:
            print(event)

    def get(self, id: int):
        return self.events[id]

    def add(self, event: Event):
        self.events.append(event)

    def get_events_by_day(self, day: datetime):
        return [event for event in self.events if event.date.date() == day.date()]

    def get_events_by_name(self, name: str):
        return [event for event in self.events if event.name == name]
