import math
import logging
from numpy import random
from Statistics import Statistics
from modules.ManupulatedOfflineWallet import ManipulatedOfflineWallet
from modules.nodes.UserNode import UserNode
from modules.Types import FRAUD_USER
from modules.Bfs import bfs_to_intermediary
from Config import InputsConfig as p
from EventOrganizer import EventOrganizer as eo
logger = logging.getLogger("CBDCSimLog")

class FraudUserNode(UserNode):
    """ Fradulent User node """
    type = FRAUD_USER
    money_sent = 0
    init_balance = 0

    def __init__(self, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)
        self.offline_target = max(int(random.normal(p.fraud_user_balance_preferance["mean"], p.fraud_user_balance_preferance["std"])), 0)
        self.ow = ManipulatedOfflineWallet()
        self.tx_rate = p.tx_rate_fraud

    def approve_recieve_offline_transaction(self,payer_node, amount):
        return True
    
    def update_connectivity(self,is_online,intermediary):
        pass

    def send_money(self):
        """ request money"""
        neigbor_choice = int(random.randint(0, len(self.neighbors)))
        target = self.neighbors[neigbor_choice]
        amount = min(self.get_offline_balance(), p.per_tx_volume_limit)
        success = self.send_offline_transaction(amount, target)
        if (success):
            balance = self.init_balance - self.money_sent
            logger.info(f"{self.node_id} {self.ow.account_id} balance {balance}, sending {amount}")
            if (amount > balance):
                if (balance <= 0):
                    Statistics.fradulent_tx_sent += 1
                    Statistics.fradulent_tx_sent_volume += amount
                else:
                    Statistics.fradulent_tx_sent += 1
                    Statistics.fradulent_tx_sent_volume += amount - balance
            self.money_sent += amount

    def _init_deposit(self):
        has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
        if has_connection_to_intermediary:
            self.trigger_reconnected(intermediary)
            balance = self.ow.get_balance()
            self.init_balance = balance
            self.init_deposit = True
            self.is_online = False

    def tick(self):
        if (not self.init_deposit):
            eo.add_event(self._init_deposit)
        if (random.poisson(1/self.tx_rate)):
            eo.add_event(self.do_transaction)