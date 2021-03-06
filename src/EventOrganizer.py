import math
from queue import Queue
from modules.Blockchain import BlockChain as bc
from Config import InputsConfig as p
from modules.events.BaseEvent import Event

class EventOrganizer:
    running = True
    event_queue = Queue()
    tick = 0
    
    def add_event(event: Event):
        EventOrganizer.event_queue.put(event)

    def event_handler(event: Event):
        event.execute()

    def event_organizer():
        while EventOrganizer.running:
            if (not EventOrganizer.event_queue.empty()):
                event = EventOrganizer.event_queue.get()
                EventOrganizer.event_handler(event)
            EventOrganizer.check_finished()
    
    def generate_events(graph):
        nodes = graph.nodes()
        loops = math.floor(p.tx_per_node*p.tx_rate)
        node_count = len(nodes)
        print("loops",loops)
        print("nodes",node_count)
        for _ in range(loops):
            EventOrganizer.tick += 1
            for node in nodes:
                nodeObject = graph.get_node(node)
                nodeObject.tick()

    def check_finished():
        if bc.get_n_of_transactions() >= p.tx_limit or EventOrganizer.event_queue.empty():
            EventOrganizer.running = False
