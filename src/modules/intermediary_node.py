""" The intermediary Node """
import operator
from modules.node import Node
from modules.types import INTERMEDIARY


class IntermediaryNode(Node):
    """ Intermediary Node processes the blockchain """
    is_online = True
    type = INTERMEDIARY

    def __init__(self, bc=None, sim=None, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)
        self.bc = bc

    def add_transaction_to_bc(self, from_account,to_account,amount):
        if (self.get_funds_of_node(from_account) <= amount):
            print("ERROR, not enough funds")
            return False
        self.bc.add_transaction(to_account, from_account, amount)

    def request_transaction(self, payee_node_id, payer_node_id, amount):
        payer_node = self.graph.get_node(payer_node_id)
        payee_node = self.graph.get_node(payee_node_id)
        if not payer_node.approve_transaction(payee_node_id, amount):
            return False
        self.add_transaction_to_bc(payer_node.account_id,payee_node.account_id,amount)

    
    def offline_deposit(self, node, amount):
        if (self.bc.balance_of(node.account_id) >= amount):
            pass
    
    def offline_withdraw(self, node, amount):
        if (self.bc.balance_of(node.get_offline_address()) >= amount):
            pass
    
    def redeem_payments(self, payments):
        payments.sort(key=operator.attrgetter("timestamp"), reverse=False)
        for payment in payments:
            # Validate certificates
            # Validate payment with signature and certificate
            self.add_transaction_to_bc(payment.sender,payment.sender,payment.amount)

    def get_funds_of_node(self, account_id):
        return self.bc.balance_of(account_id)
    
    def tick(self):
        pass