from numpy import random
from modules.node import Node
from modules.types import USER
from modules.bfs import bfs_to_intermediary
from config import InputsConfig as p

class UserNode(Node):
    """ User node """
    transactions = dict()
    type = USER
    def __init__(self, sim=None, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)
        self.sim = sim
        self.tx_rate = p.tx_rate
        self.node_id = node_id

    def request_money(self):
        has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
        if (has_connection_to_intermediary):
            neigbor_choice = int(random.randint(0, len(self.neighbors)))
            target = self.neighbors[neigbor_choice]
            amount = random.randint(1, 100)
            intermediary.request_transaction(self.node_id, target, amount)
            # Get nearby user to give money

    def get_closest_intermediary(self):
        return bfs_to_intermediary(self.graph.nodes, self.node_id)

    
    def approve_transaction(self,from_node_id, amount):
        # Some algorithm for determining if node wants to pay
        return True
    
    def do_transaction(self):
        # Get closest intermediary only transiting routers
        # Get nearby user to give money
        # Send money, amount = 

        #print(f"transaction {self.id}")
        self.request_money()

    def get_balance(self):
        has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
        if (has_connection_to_intermediary):
            return True, intermediary.get_funds_of_node(self.account_id)
        return False, 0

    def tick(self):
        if (random.random() <= self.tx_rate):
            self.sim.add_event(self.do_transaction)

    def remove_from_balance(self):
        pass

    def add_to_balance(self):
        pass
