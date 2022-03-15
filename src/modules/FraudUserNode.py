import math
import logging
from numpy import random
from Statistics import Statistics
from modules.ManupulatedOfflineWallet import ManipulatedOfflineWallet
from modules.UserNode import UserNode
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


    def approve_recieve_offline_transaction(self,payer_node, amount):
        return True

    def send_money(self):
        """ request money"""
        neigbor_choice = int(random.randint(0, len(self.neighbors)))
        target = self.neighbors[neigbor_choice]
        amount = self.get_offline_balance()
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

    def do_transaction(self):
        self.send_money()
        if (not self.init_deposit):
            self.check_online()
            if (self.is_online):
                self.trigger_reconnected(self.closest_intermediary)
            balance = self.ow.get_balance()
            self.init_balance = balance
            self.init_deposit = True
            self.is_online = False
    
    def check_online(self):
        if (not self.init_deposit):
            has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
            self.is_online = has_connection_to_intermediary
            self.closest_intermediary = intermediary
            self.update_connectivity(has_connection_to_intermediary, intermediary)
        return True

    def tick(self):
        if (random.poisson(1/p.tx_rate_fraud)):
            eo.add_event(self.do_transaction)
