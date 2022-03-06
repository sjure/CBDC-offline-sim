from modules.node import Node
from modules.types import INTERMEDIARY
import secrets
from numpy import random

class IntermediaryNode(Node):
        is_online = True
        type = INTERMEDIARY

        def __init__(self, bc=None, sim=None, node_id=-1,**attr):
            super().__init__(node_id=node_id, **attr)
            self.bc = bc

        def request_transaction(self, payee_node_id, payer_node_id, amount):
            payer_node = self.graph.get_node(payer_node_id)
            payee_node = self.graph.get_node(payee_node_id)
            if not payer_node.approve_transaction(payee_node_id, amount):
                return False
            if (self.get_funds_of_node(payer_node.account_id) <= amount):
                return False
            self.bc.add_transaction(payee_node.account_id, payer_node.account_id, amount)

        def get_funds_of_node(self, account_id):
            return self.bc.balance_of(account_id)
        
        def tick(self):
            pass
        


        