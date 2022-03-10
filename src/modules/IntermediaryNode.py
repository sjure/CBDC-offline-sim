""" The intermediary Node """
import operator
from numpy.random import poisson, exponential
from modules.BaseNode import Node
from modules.Types import INTERMEDIARY
from modules.Blockchain import BlockChain as bc
from Config import InputsConfig as p

class IntermediaryNode(Node):
    """ Intermediary Node processes the blockchain """
    is_online = True
    ticks_to_online = 0
    current_offline_ticks = 0
    type = INTERMEDIARY

    def __init__(self, sim=None, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)

    def add_transaction_to_bc(self, from_account,to_account,amount):
        if (self.get_funds_of_node(from_account) < amount):
            print("ERROR, not enough funds", self.get_funds_of_node(from_account), amount)
            return False
        bc.add_transaction(to_account, from_account, amount)

    def request_transaction(self, payee_node_id, payer_node_id, amount):
        payer_node = self.graph.get_node(payer_node_id)
        payee_node = self.graph.get_node(payee_node_id)
        if not payer_node.approve_transaction(payee_node_id, amount):
            return False
        self.add_transaction_to_bc(payer_node.account_id,payee_node.account_id,amount)

    
    def offline_deposit(self, node, amount):
        self.add_transaction_to_bc(node.account_id,node.get_offline_address(),amount)
        return ""

    def offline_withdraw(self, node, amount, signature):
        # Verify signature of Secure hardware deletion of funds
        return self.add_transaction_to_bc(node.get_offline_address(),node.account_id, amount)
        
    
    def redeem_payments(self, payments):
        payments.sort(key=operator.attrgetter("timestamp"), reverse=False)
        for payment in payments:
            # Validate certificates
            # Validate payment with signature and certificate
            self.add_transaction_to_bc(payment.sender,payment.sender,payment.amount)

    def get_funds_of_node(self, account_id):
        return bc.balance_of(account_id)

    def tick(self):
        """ Tick method of intermediary node """
        if self.is_online:
            if (poisson(1/p.intermediary_failure_rate)):
                self.is_online = False
                print("intermediary offline")
                self.ticks_to_online = exponential(p.intermediary_recovery_rate)
        else:
            self.current_offline_ticks += 1
            if (self.current_offline_ticks >= self.ticks_to_online):
                self.is_online = True
                print("intermediary online")
                self.current_offline_ticks = 0
                self.ticks_to_online = 0

