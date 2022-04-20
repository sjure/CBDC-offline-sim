import math
import logging
from numpy import random
from Statistics import Statistics
from modules.events.UserEvent import UserEvent
from modules.wallets.ManupulatedOfflineWallet import ManipulatedOfflineWallet
from modules.nodes.UserNode import UserNode
from modules.Types import FRAUD_USER
from modules.Bfs import bfs_to_intermediary
from Config import InputsConfig as p
from EventOrganizer import EventOrganizer as eo
from modules.wallets.OfflineWallet import OfflinePayment
logger = logging.getLogger("CBDCSimLog")


class FraudUserNode(UserNode):
    """ Fradulent User node """
    type = FRAUD_USER
    money_sent = 0
    init_balance = 0
    fraud_sendt = 0
    fradulent_wallet_active = False

    def __init__(self, node_id=-1, **attr):
        super().__init__(node_id=node_id, **attr)
        self.offline_target = max(int(random.normal(
            p.fraud_user_balance_preferance["mean"], p.fraud_user_balance_preferance["std"])), 0)
        self.ow = ManipulatedOfflineWallet()
        self.tx_rate = p.tx_rate_fraud

    def approve_recieve_offline_transaction(self, payer_node, amount):
        return True

    def update_connectivity(self, is_online, intermediary):
        pass

    def offline_sufficient_funds(self, amount):
        return True

    def send_money(self):
        """ request money"""
        neigbor_choice = int(random.randint(0, len(self.neighbors)))
        target = self.neighbors[neigbor_choice]
        amount = min(self.init_balance, p.per_tx_amount_limit)
        balance = self.init_balance - self.money_sent
        if (balance < amount):
            self.fradulent_wallet_active = True
            self.ow.reset(p.per_tx_amount_limit)
        if (self.fradulent_wallet_active):
            self.payment_log = self.payment_log[:1]
            Statistics.fradulent_tx_attempted_sent += 1
            Statistics.fradulent_tx_attempted_sent_volume += amount
        success = self.send_offline_transaction(amount, target)
        if (success):
            logger.info(
                f"{self.ow.account_id} {self.ow.counter} balance {balance}, sending {amount}, counter={self.ow.counter} to {target.ow.account_id} ")
            Statistics.offline_tx += 1
            Statistics.offline_tx_volume += amount
            if (balance < amount):
                Statistics.fradulent_tx_sent += 1
                Statistics.fradulent_tx_sent_volume += amount
                self.fraud_sendt += amount
            self.money_sent += amount
        else:
            logger.info(
                f"{self.ow.account_id} {self.ow.counter} unsuccessfull")
            logger.info(self.payment_log)

        if (amount <= balance and not success):
            print(balance, self.fradulent_wallet_active)

    def receive_payment(self, payment_received: OfflinePayment, payment_log):
        return self.ow.collect(payment_received)

    def _init_deposit(self):
        has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
        if has_connection_to_intermediary:
            if not self.init_deposit:
                self.trigger_reconnected(intermediary)
                balance = self.ow.get_balance()
                self.init_balance = balance
                self.init_deposit = True
                self.is_online = False

    def tick(self):
        if (not self.init_deposit):
            eo.add_event(UserEvent(self._init_deposit))
        if (random.poisson(1/self.tx_rate)):
            eo.add_event(UserEvent(self.do_transaction))
