from modules.events.BaseEvent import Event


class NetworkEvent(Event):
    """ Network event"""
    def __init__(self, method):
        self.method = method

    def execute(self):
        self.method()
