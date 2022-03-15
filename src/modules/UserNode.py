import math
import logging
from numpy import random
from Statistics import Statistics
from modules.BaseNode import Node
from modules.Types import USER
from modules.Bfs import bfs_to_intermediary
from Config import InputsConfig as p
from EventOrganizer import EventOrganizer as eo
logger = logging.getLogger("CBDCSimLog")

class UserNode(Node):
    """ User node """
    transactions = dict()
    is_online = False
    init_deposit = False
    type = USER
    def __init__(self, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)
        self.node_id = node_id
        self.offline_target = max(int(random.normal(p.offline_balance_preferance["mean"], p.offline_balance_preferance["std"])), 0)

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

    def approve_recieve_offline_transaction(self,payer_node, amount):
        if (self.is_online):
            return self.closest_intermediary.is_valid_tx(payer_node.get_offline_address(), amount)
        else:
            return True

    def send_offline_transaction(self, amount, target):
        if amount <= 0:
            return False
        target_accepts_transaction = target.approve_recieve_offline_transaction(self, amount)
        if (target_accepts_transaction):
            success, payment, payment_log = self.create_offline_transaction(amount, self)
            if (success):
                Statistics.offline_tx += 1
                Statistics.offline_tx_volume += payment.tx.amount
                logger.info(f"Offline transaction from {payment.tx.from_address} to {payment.tx.to_address} amount {amount}")
                target.ow.collect(payment)
                target.ow.sync_payment_log(payment_log)
                return True
            else:
                logger.info(f"no transaction, node-id={self.node_id} amount={amount}, offline-bal={self.get_offline_balance()}")
        else:
            logger.info(f"Target did not accept transaction target={target.get_offline_address()} amount={amount} from={self.get_offline_address()}")
        return False

    def send_money(self):
        """ request money"""
        neigbor_choice = int(random.randint(0, len(self.neighbors)))
        target = self.neighbors[neigbor_choice]
        amount = max(int(random.normal(p.tx_volume["mean"], p.tx_volume["std"])),1)
        self.check_online()
        target.check_online()
        if (self.is_online and target.is_online):
            # Do online transaction, both users can check the validity in the intermediary
            self.closest_intermediary.send_transaction(self.node_id, target.node_id, amount)
        elif (self.is_online and not target.is_online):
            is_valid, tx, sign = self.closest_intermediary.send_transaction(self.node_id, target.node_id, amount)
            if (is_valid):
                target.recieve_confirmation(tx,sign)
        elif (not self.is_online and target.is_online):
            logger.info("Offline tx with online check")
            self.send_offline_transaction(amount, target)
        else:
            logger.info("Offline tx")
            self.send_offline_transaction(amount, target)

    def recieve_confirmation(self,tx,sign):
        # Check signature of intermediary with intermediary certificate
        return len(sign)

    def create_offline_transaction(self,amount,reciever):
        if (self.offline_sufficient_funds(amount)):
            address = reciever.get_offline_address()
            payment = self.ow.pay(amount, address)
            payment_log = self.ow.get_payment_log()
            return True, payment, payment_log
        return False, None, []

    def offline_sufficient_funds(self, amount):
        if (self.get_offline_balance() < amount):
            return False
        return True

    def get_offline_balance(self):
        return self.ow.get_balance()
    
    def get_offline_address(self):
        return self.ow.account_id

    def get_closest_intermediary(self):
        return bfs_to_intermediary(self)
    
    def do_transaction(self):
        # Get closest intermediary only transiting routers
        # Get nearby user to give money
        # Send money, amount = 

        #print(f"transaction {self.id}")
        self.send_money()
        if (not self.init_deposit):
            self.check_online()
            if (self.is_online):
                self.trigger_reconnected(self.closest_intermediary)
            self.init_deposit = Trueamount
    

    def check_online(self):
        has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
        self.is_online = has_connection_to_intermediary
        self.closest_intermediary = intermediary
        self.update_connectivity(has_connection_to_intermediary, intermediary)

    def get_balance(self):
        has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
        if (has_connection_to_intermediary):
            return True, intermediary.get_funds_of_node(self.account_id)
        return False, 0

    def tick(self):
        if (random.poisson(1/p.tx_rate)):
            eo.add_event(self.do_transaction)
