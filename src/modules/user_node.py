from modules.node import Node
from modules.types import USER
import secrets
from numpy import random
from modules.bfs import BFS_to_intermediary

class UserNode(Node):
    transactions = dict()
    type = USER
    def __init__(self, sim=None, tx_rate=0.1, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)
        self.sim = sim
        self.tx_rate = tx_rate
        self.node_id = node_id

    def request_money(self):
        has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
        if (has_connection_to_intermediary):
            target = self.neighbors[random.randint(0, len(self.neighbors))]
            amount = random.randint(1, 100)
            intermediary.request_transaction(self.node_id, target, amount)
            # Get nearby user to give money

    def get_closest_intermediary(self):
        return BFS_to_intermediary(self.graph.nodes, self.node_id)

    
    def approve_transaction(self,from_node_id, amount):
        return True
    
    def do_transaction(self):
        # Get closest intermediary only transiting routers
        # Get nearby user to give money
        # Send money, amount = 

        #print(f"transaction {self.id}")
        self.request_money()

    def get_balance(self):
        return self.bc.balance_of(self.account_id)

    def tick(self):
        if (random.random() <= self.tx_rate):
            self.sim.add_event(self.do_transaction)

    def remove_from_balance(self):
        pass

    def add_to_balance(self):
        pass

    def approve_transaction(self, to, amount):
        # Some algorithm for determining if node wants to pay
        return True
    
