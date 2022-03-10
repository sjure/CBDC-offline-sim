import math
from numpy import random
from modules.node import Node
from modules.types import USER
from modules.bfs import bfs_to_intermediary
from Config import InputsConfig as p

class UserNode(Node):
    """ User node """
    transactions = dict()
    is_online = False
    type = USER
    def __init__(self, sim=None, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)
        self.sim = sim
        self.tx_rate = p.tx_rate
        self.node_id = node_id
        self.offline_target = max(random.normal(p.offline_balance_preferance["mean"], p.offline_balance_preferance["std"]), 0)
    
    def redeem_offline_transactions(self,intermediary):
        payments = self.ow.redeem_payments()
        intermediary.redeem_payments(payments)

    def trigger_reconnected(self, intermediary):
        offline_balance = self.get_offline_balance()
        if (offline_balance == self.offline_target):
            return
        self.redeem_offline_transactions(intermediary)
        is_online, online_balance = self.get_balance()
        if not is_online or online_balance == 0:
            return

        if offline_balance < self.offline_target:
            diff_from_target = self.offline_target - offline_balance
            if diff_from_target <= online_balance:
                signature = intermediary.offline_deposit(self,diff_from_target)
                self.ow.deposit(diff_from_target, self.account_id,signature)
            else:
                signature = intermediary.offline_deposit(self,online_balance)
                self.ow.deposit(online_balance, self.account_id,signature)
        else:
            diff_from_target = offline_balance - self.offline_target
            signature = self.ow.withdraw(self.account_id, diff_from_target)
            intermediary.offline_withdraw(self, diff_from_target, signature)

    def update_connectivity(self,is_online,intermediary):
        if (self.is_online == is_online):
            return
        was_offline = not self.is_online
        if (was_offline and is_online):
            self.trigger_reconnected(intermediary)
        self.is_online = is_online

    def request_money(self):
        """ request money"""
        neigbor_choice = int(random.randint(0, len(self.neighbors)))
        target = self.neighbors[neigbor_choice]
        amount = random.randint(1, 100)
        has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
        self.update_connectivity(has_connection_to_intermediary, intermediary)
        if (has_connection_to_intermediary):
            # Get nearby user to give money
            intermediary.request_transaction(self.node_id, target.node_id, amount)
        else:
            print("OFFLINE")
            self.request_offline_transaction(amount, target)

    def request_offline_transaction(self, amount, sender):
        success, payment, payment_log = sender.offline_transaction(amount, self)
        if (success):
            self.ow.collect(payment)
            self.ow.sync_payment_log(payment_log)
        else:
            print("no transaction")
    
    def offline_transaction(self,amount,reciever):
        if (self.approve_offline_transaction(amount, reciever)):
            address = reciever.get_offline_address()
            payment = self.ow.pay(amount, address)
            payment_log = self.ow.get_payment_log()
            return True, payment, payment_log
        return False, None, []

    def approve_offline_transaction(self, amount, reciever):
        if (self.get_offline_balance() < amount):
            return False
        return self.approve_transaction(reciever, amount)

    def get_offline_balance(self):
        return self.ow.get_balance()
    
    def get_offline_address(self):
        return self.ow.account_id

    def get_closest_intermediary(self):
        return bfs_to_intermediary(self)

    
    def approve_transaction(self,from_node_id, amount):
        # Some algorithm for determining if node wants to pay
        has_connection, balance = self.get_balance()
        if (balance >= amount):
            return True
        return False
    
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
