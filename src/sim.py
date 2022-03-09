import math
import logging
from queue import Queue
from numpy import random
from modules.barabasi_albert import BarabasiAlbert
from modules.types import NETWORK, INTERMEDIARY
from config import InputsConfig as p

LOGGING_FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,datefmt="%H:%M:%S")

graphs = {
    "ba": BarabasiAlbert,
}

class Simulate():
    """ Simulation class """
    def __init__(self):
        self.event_queue = Queue()
        self.running = True
        graph_type = p.graph_type
        graph_params = p.graph_params
        self.graph = graphs[graph_type](sim=self,**graph_params)
        self.tx_limit = p.tx_limit
        self.tx_per_node = p.tx_per_node
        self.tx_rate = p.tx_rate
        self.add_init_balance(p.balance["mean"], p.balance["std"])
        print("init blocks", len(self.graph.bc.blocks))
        self.print_all_balances()
        self.generate_events()
        print("events",self.event_queue.qsize())
        self.event_organizer()
        print("total blocks", len(self.graph.bc.blocks))
        print("blocks", self.graph.bc.blocks)
        print("blocks", self.graph.bc.verify_block_chain())
        self.print_all_balances()
    
    
    def print_all_balances(self):
        sum_of_balances = 0
        for node_id in self.graph.nodes:
            node = self.graph.get_node(node_id)
            bal = self.graph.bc.balance_of(node.account_id)
            sum_of_balances += bal
            print(node_id, " balance ", bal)
        print("Sum of all balances", sum_of_balances)


    def add_init_balance(self,mean,std):
        for node in self.graph.nodes():
            if (self.graph.nodes[node]["data"].type in [NETWORK,INTERMEDIARY]):
                continue
            wallet_id = self.graph.nodes[node]["data"].account_id
            wallet_amount = random.normal(mean,std)
            if (wallet_amount < 0):
                wallet_amount=0
            self.graph.bc.deposit_money(wallet_id, wallet_amount)

    def add_event(self,event):
        self.event_queue.put(event)

    def event_handler(self,event):
        event()

    def event_organizer(self):
        while self.running:
            if (self.event_queue.not_empty):
                event = self.event_queue.get()
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
        if self.graph.bc.get_n_of_transactions() >= self.tx_limit or self.event_queue.empty:
            self.running = False


if __name__ == "__main__":
    simulator = Simulate()