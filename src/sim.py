import math
import threading
from modules.barabasi_albert import BarabasiAlbert
import logging
import time
from numpy import random
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

graphs = {
    "ba": BarabasiAlbert,
}

class Simulate():
    def __init__(self,**config_dict):
        self.event_queue = []
        self.running = True
        graph_type = config_dict["graph"]["type"]
        graph_params = config_dict["graph"]["params"]
        self.graph = graphs[graph_type](sim=self,**graph_params,**config_dict)
        self.tx_limit = config_dict["tx_limit"]
        self.tx_per_node = config_dict["tx_per_node"]
        self.tx_rate = config_dict["tx_rate"]
        self.add_init_balance(config_dict["balance"]["mean"], config_dict["balance"]["std"])
        print("init blocks", len(self.graph.bc.blocks))
        self.generate_events()
        print("events",len(self.event_queue))
        self.event_organizer()
    
    def add_init_balance(self,mean,std):
        for node in self.graph.nodes():
            wallet_id = self.graph.nodes[node]["data"].id
            wallet_amount = random.normal(mean,std)
            if (wallet_amount < 0):
                wallet_amount=0
            self.graph.bc.deposit_money(wallet_id, wallet_amount)

    def add_event(self,event):
        self.event_queue.append(event)

    def event_handler(self,event):
        event()

    def event_organizer(self):
        while self.running:
            if (len(self.event_queue)):
                event = self.event_queue.pop(0)
                self.event_handler(event)
            self.check_finished()
    
    def generate_events(self):
        loops = math.floor(self.tx_per_node/ self.tx_rate)
        nodes = len(self.graph.nodes())
        print("loops",loops)
        print("nodes",nodes)
        for _ in range(loops):
            for node in self.graph.nodes():
                nodeObject = self.graph.nodes[node]["data"]
                nodeObject.tick()

    def check_finished(self):
        if self.graph.bc.get_n_of_transactions() >= self.tx_limit or len(self.event_queue) == 0 :
            self.running = False


if __name__ == "__main__":
    from config import config_dict
    simulator = Simulate(**config_dict)

    