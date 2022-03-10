import math
import logging
from queue import Queue
from numpy import random
from modules.barabasi_albert import BarabasiAlbert
from modules.types import NETWORK, INTERMEDIARY, USER
from config import InputsConfig as p
from modules.blockchain import BlockChain as bc

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
        print("init blocks", len(bc.blocks))
        self.print_all_balances()
        self.generate_events()
        print("events",self.event_queue.qsize())
        self.event_organizer()
        print("total blocks", len(bc.blocks))
        #print("blocks", self.graph.bc.blocks)
        print("All blocks authentic", bc.verify_block_chain())
        self.print_all_balances()
    
    
    def print_all_balances(self):
        sum_of_balances = 0
        sum_of_offline = 0
        print("Node".ljust(5) + "Active balance".ljust(25) + "Offline balance".ljust(15))
        for node_id in self.graph.nodes:
            node = self.graph.get_node(node_id)
            online_balance = bc.balance_of(node.account_id)
            sum_of_balances += online_balance
            if node.type == USER:
                offline_bal = bc.balance_of(node.get_offline_address())
                sum_of_offline += offline_bal
                print(str(node_id).ljust(5) + str(online_balance).ljust(25) + str(offline_bal).ljust(15))
        print("Sum of all online balances", sum_of_balances)
        print("Sum of all offline", sum_of_offline)
        print("Sum of all", sum_of_offline + sum_of_balances)


    def add_init_balance(self,mean,std):
        for node in self.graph.nodes():
            if (self.graph.nodes[node]["data"].type in [NETWORK,INTERMEDIARY]):
                continue
            wallet_id = self.graph.nodes[node]["data"].account_id
            wallet_amount = random.normal(mean,std)
            if (wallet_amount < 0):
                wallet_amount=0
            bc.deposit_money(wallet_id, wallet_amount)

    def add_event(self,event):
        self.event_queue.put(event)

    def event_handler(self,event):
        event()

    def event_organizer(self):
        while self.running:
            if (not self.event_queue.empty()):
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
        if bc.get_n_of_transactions() >= self.tx_limit or self.event_queue.empty():
            self.running = False


if __name__ == "__main__":
    simulator = Simulate()
