from modules.node import Node
from modules.types import USER
import secrets
from numpy import random

class UserNode(Node):
    transactions = dict()
    type = USER
    def __init__(self, bc=None, sim=None, tx_rate=0.1, node_id=-1):
        self.bc = bc
        self.sim = sim
        self.tx_rate = tx_rate
        self.node_id = node_id
        self.id = secrets.token_hex(16)

    def request_money(self):
        # Get closest intermediary only transiting routers
        # Get nearby user to give money

        pass
    
    def do_transaction(self):
        # Get closest intermediary only transiting routers
        # Get nearby user to give money
        # Send money, amount = 

        #print(f"transaction {self.id}")
        pass

    def get_balance(self):
        return self.bc.balance_of(self.id)

    def tick(self):
        if (random.random() >= self.tx_rate):
            self.sim.add_event(self.do_transaction)

    def remove_from_balance(self):
        pass

    def add_to_balance(self):
        pass
    
