""" The intermediary Node """
import operator
import logging
from numpy.random import poisson, exponential
from modules.BaseNode import Node
from modules.Types import INTERMEDIARY
from modules.Blockchain import BlockChain as bc
from Config import InputsConfig as p
from Statistics import Statistics
from EventOrganizer import EventOrganizer as eo
logger = logging.getLogger("CBDCSimLog")

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
            logger.error(f"ERROR, not enough funds {self.get_funds_of_node(from_account)}, {amount}")
            return False
        bc.add_transaction(to_account, from_account, amount)

    def send_transaction(self, payee_node_id, payer_node_id, amount):
        payer_node = self.graph.get_node(payer_node_id)
        payee_node = self.graph.get_node(payee_node_id)
        if not payee_node.approve_transaction(payer_node_id, amount):
            return False
        Statistics.online_tx += 1
        Statistics.online_tx_volume += amount
        logger.info(f"Online transaction from {payer_node_id} to {payee_node_id} amount {amount}")
        self.add_transaction_to_bc(payer_node.account_id,payee_node.account_id,amount)

    
    def offline_deposit(self, node, amount):
        logger.info(f"Depost to offline wallet from {node.account_id} to {node.get_offline_address()} amount {amount}")
        self.add_transaction_to_bc(node.account_id,node.get_offline_address(),amount)
        return ""

    def offline_withdraw(self, node, amount, signature):
        logger.info(f"Withdrawal from offline wallet from {node.account_id} to {node.get_offline_address()} amount {amount}")
        # Verify signature of Secure hardware deletion of funds
        return self.add_transaction_to_bc(node.get_offline_address(),node.account_id, amount)
        
    
    def redeem_payments(self, payments):
        payments.sort(key=operator.attrgetter("timestamp"), reverse=False)
        logger.info(f"Redeem payemnts {payments}")
        for payment in payments:
            # Validate certificates
            # Validate payment with signature and certificate
            if not bc.has_transaction(payment.tx.id):
                bc.add_transaction_from_offline(payment.tx)

    def get_funds_of_node(self, account_id):
        return bc.balance_of(account_id)


    def handle_fault(self):
        if self.is_online:
            if (poisson(1/p.intermediary_failure_rate)):
                self.is_online = False
                logger.info("intermediary -> offline")
                self.ticks_to_online = int(exponential(p.intermediary_recovery_rate))
                logger.info(f"{self.ticks_to_online} ticks to online")
                Statistics.intermediary_failures += 1
        else:
            self.current_offline_ticks += 1
            if (self.current_offline_ticks >= self.ticks_to_online):
                self.is_online = True
                logger.info("intermediary -> online")
                self.current_offline_ticks = 0
                self.ticks_to_online = 0
                Statistics.intermediary_repairs += 1


    def tick(self):
        """ Tick method of intermediary node """
        eo.add_event(self.handle_fault)
