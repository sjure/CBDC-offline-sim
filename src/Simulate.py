import logging
from numpy import random
from modules.BarabasiAlbert import BarabasiAlbert
from modules.Types import NETWORK, INTERMEDIARY, USER
from Config import InputsConfig as p
from modules.Blockchain import BlockChain as bc
from EventOrganizer import EventOrganizer as eo

LOGGING_FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,datefmt="%H:%M:%S")

graphs = {
    "ba": BarabasiAlbert,
}

class Simulate():
    """ Simulation class """
    def __init__(self):
        graph_type = p.graph_type
        graph_params = p.graph_params
        self.graph = graphs[graph_type](sim=self,**graph_params)
        self.add_init_balance(p.balance["mean"], p.balance["std"])
        print("init blocks", len(bc.blocks))
        self.print_all_balances()
        eo.generate_events(self.graph, self.graph.nodes())
        print("events", eo.event_queue.qsize())
        eo.event_organizer()
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


if __name__ == "__main__":
    simulator = Simulate()
