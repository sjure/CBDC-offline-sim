from modules.events.BaseEvent import Event


class UserEvent(Event):
    """ User event"""
    def __init__(self, method):
        self.method = method

    def execute(self):
        self.method()
