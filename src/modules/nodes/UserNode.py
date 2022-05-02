import math
import logging
from numpy import random
import hashlib
from Statistics import Statistics
from modules.events.UserEvent import UserEvent
from modules.nodes.BaseNode import Node
from modules.Types import USER
from modules.Bfs import bfs_to_intermediary
from Config import InputsConfig as p
from EventOrganizer import EventOrganizer as eo
from modules.sort.SortPayments import sort_payments
from modules.wallets.OfflineWallet import OfflinePayment, UserBal
logger = logging.getLogger("CBDCSimLog")


class UserNode(Node):
    """ User node """
    is_online = False
    init_deposit = False
    type = USER

    def __init__(self, node_id=-1, **attr):
        super().__init__(node_id=node_id, **attr)
        self.node_id = node_id
        self.offline_target = max(int(random.normal(
            p.offline_balance_preferance["mean"], p.offline_balance_preferance["std"])), 0)
        self.tx_rate = p.tx_rate
        self.payment_log = []
        self.ban_list = set()
        self.local_ban_list = set()
        self.fradulent_tx = []
        self.bc_random = random.RandomState(p.random_seed)

    def redeem_offline_transactions(self, intermediary):
        payments = self.payment_log
        ban_list = intermediary.redeem_payments(payments, self)
        if p.lockout_after_consolidation:
            self.ban_list = ban_list

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
                success, tx, signature = intermediary.offline_deposit(
                    self, diff_from_target)
                offline_payment = self.ow.deposit(tx, signature)
                self.payment_log.append(offline_payment)
            else:
                success, tx, signature = intermediary.offline_deposit(
                    self, online_balance)
                offline_payment = self.ow.deposit(tx, signature)
                self.payment_log.append(offline_payment)
        else:
            diff_from_target = offline_balance - self.offline_target
            withdraw_payment = self.ow.withdraw(
                self.account_id, diff_from_target)
            self.payment_log.append(withdraw_payment)
            intermediary.offline_withdraw(self, withdraw_payment)

    def update_connectivity(self, is_online, intermediary):
        if (self.is_online == is_online):
            return
        was_offline = not self.is_online
        if (was_offline and is_online):
            self.trigger_reconnected(intermediary)
        self.is_online = is_online
        self.closest_intermediary = intermediary

    def check_payer_node(self, payer_node, amount):
        if p.client_preventions:
            if payer_node.get_offline_address() in self.local_ban_list:
                Statistics.fradulent_tx_client_prevention_prevented += 1
                Statistics.fradulent_tx_client_prevention_prevented_volume += amount
                logger.info(
                    f"ERROR: payer address in local ban list {payer_node.get_offline_address()}")
                return False
        if p.lockout_after_consolidation:
            if payer_node.get_offline_address() in self.ban_list:
                Statistics.fradulent_tx_server_lockout_prevented += 1
                Statistics.fradulent_tx_server_lockout_prevented_volume += amount
                logger.info(
                    f"ERROR: payer address in ban list {payer_node.get_offline_address()}")
                return False
        return True

    def approve_recieve_offline_transaction(self, payer_node, amount):
        if (amount > p.per_tx_amount_limit):
            print("OVER LIMIT")
            return False
        if (self.is_online):
            isValid = self.closest_intermediary.is_valid_tx(
                payer_node.get_offline_address(), amount)
            if not isValid:
                Statistics.fradulent_tx_client_online_check += 1
                Statistics.fradulent_tx_client_online_check_volume += amount
            return isValid
        return self.check_payer_node(payer_node, amount)

    def send_offline_transaction(self, amount, target):
        if amount <= 0:
            return False
        target_accepts_transaction = target.approve_recieve_offline_transaction(
            self, amount)
        if (target_accepts_transaction):
            success, payment, payment_log = self.create_offline_transaction(
                amount, target)
            if (success):
                logger.info(
                    f"Offline transaction from {payment.tx.from_address} {payment.tx.counter} to {payment.tx.to_address} amount {amount}")
                pm_success = target.receive_payment(payment, payment_log)
                if not pm_success:
                    Statistics.fradulent_tx_client_prevention_prevented += 1
                    Statistics.fradulent_tx_client_prevention_prevented_volume += amount
                return pm_success
            else:
                logger.info(
                    f"no transaction, target={target.get_offline_address()} amount={amount} from={self.get_offline_address()}, offline-bal={self.get_offline_balance()}")
        else:
            logger.info(
                f"Target did not accept transaction target={target.get_offline_address()} amount={amount} from={self.get_offline_address()}")
        return False

    def send_money(self):
        """ request money"""
        neigbor_choice = int(random.randint(0, len(self.neighbors)))
        target = self.neighbors[neigbor_choice]
        amount = min(max(int(random.normal(
            p.tx_volume["mean"], p.tx_volume["std"])), 1),  p.per_tx_amount_limit)
        self.check_online()
        target.check_online()
        if (self.is_online and target.is_online):
            if (self.balance < amount):
                return
            # Do online transaction, both users can check the validity in the intermediary
            self.closest_intermediary.send_transaction(
                self.node_id, target.node_id, amount)
        elif (self.is_online and not target.is_online):
            if (self.balance < amount):
                return
            # If the payee is offline, the payer will confirm the transaction with the intermediary
            # and send the signatrue as a receipt
            is_valid, tx, sign = self.closest_intermediary.send_transaction(
                self.node_id, target.node_id, amount)
            if (is_valid):
                target.recieve_confirmation(tx, sign)
        else:
            if (self.get_offline_balance() < amount):
                return
            # The case if both are offline, and if self is offline and receiver is online
            logger.info("Offline tx")
            success = self.send_offline_transaction(amount, target)
            if success:
                Statistics.offline_tx += 1
                Statistics.offline_tx_volume += amount

    def recieve_confirmation(self, tx, sign):
        # Check signature of intermediary with intermediary certificate
        return len(sign)

    def create_offline_transaction(self, amount, reciever):
        if (self.offline_sufficient_funds(amount)):
            address = reciever.get_offline_address()
            payment = self.ow.pay(amount, address)
            self.payment_log.append(payment)
            payment_log = self.get_payment_log()
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
        """ Do transaction as main method of the user node """
        self.send_money()

    def check_online(self):
        has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
        self.update_connectivity(has_connection_to_intermediary, intermediary)
        if (has_connection_to_intermediary):
            self.balance = intermediary.get_funds_of_node(self.account_id)

    def get_balance(self):
        has_connection_to_intermediary, intermediary = self.get_closest_intermediary()
        if (has_connection_to_intermediary):
            return True, intermediary.get_funds_of_node(self.account_id)
        return False, 0

    def validate_log(self, payment_log):
        """ Validate the payment log """
        if (len(payment_log) == 0):
            return False, None
        payment_log.sort(key=lambda x: x.ts)
        node_sums = {}
        fradulent_tx = []
        for payment in payment_log:
            node_sums[payment.tx.from_address] = UserBal(
                0, 0, payment.tx.from_address)
            node_sums[payment.tx.to_address] = UserBal(
                0, 0, payment.tx.to_address)
        for payment_index, payment in enumerate(payment_log):
            # Validate signature of payment
            tx = payment.tx
            if node_sums[tx.from_address].counter >= tx.counter:
                logger.info(f"ERROR: counter is not correct {tx}")
                fradulent_tx.append(payment)
                continue
            node_sums[tx.from_address].counter = tx.counter
            node_sums[tx.to_address].balance += tx.amount
            if not tx.depositType:
                transaction_hash = tx.create_hash()
                previous_hash = node_sums[tx.from_address].prev_hash
                combined_hash = hashlib.sha256(
                    transaction_hash.encode('utf-8') + previous_hash.encode('utf-8')).hexdigest()
                if combined_hash != payment.signature:
                    logger.info(f"ERROR: Hash signature is not correct {tx}")
                    logger.info(f"payments = {payment_log[0:payment_index]}")
                    fradulent_tx.append(payment)
                    continue
                node_sums[tx.from_address].balance -= tx.amount
                if node_sums[tx.from_address].balance < 0:
                    logger.info(
                        f"User balance less than zero, tx={tx}, node_sums={node_sums}")
                    logger.info(f"payments = {payment_log[0:payment_index]}")
                    fradulent_tx.append(payment)
                    continue
                node_sums[tx.from_address].prev_hash = tx.hash

        if len(fradulent_tx):
            return False, fradulent_tx
        return True, []

    def receive_payment(self, payment_received: OfflinePayment, payment_log):
        # Temporary log to check together
        # If the sender of the payments is not fradulent in the log, then the payment is valid
        combined_log = self.payment_log.copy()
        for pm in payment_log:
            if pm not in combined_log:
                combined_log.append(pm)
        if p.client_preventions:
            successfull_validate, fradulent_tx = self.validate_log(
                combined_log)
            if not successfull_validate:
                for pm in fradulent_tx:
                    tx = pm.tx
                    logger.info(
                        f"Unsuccessfull validate payment after sync, fraudster {tx.from_address}")
                    if pm not in self.fradulent_tx:
                        self.fradulent_tx.append(pm)
                    if tx.from_address == payment_received.tx.from_address:
                        self.local_ban_list.add(
                            payment_received.tx.from_address)
                        logger.info(
                            f"Add {payment_received.tx.from_address} to blacklist. New blacklist {self.local_ban_list}")
                        return False
        self.payment_log = combined_log
        success = self.ow.collect(payment_received)

        if p.collaberative_security:
            self.broadcast_logs()

        return success

    def sync_logs(self, payment_log, sender):
        combined_log = self.payment_log.copy()
        for pm in payment_log:
            if pm not in combined_log:
                combined_log.append(pm)
        successfull_validate, fradulent_tx = self.validate_log(
            combined_log)
        if not successfull_validate:
            for pm in fradulent_tx:
                tx = pm.tx
                logger.info(
                    f"Unsuccessfull validate incomming broadcast fraudster {tx.from_address}")
                if pm not in self.fradulent_tx:
                    self.fradulent_tx.append(pm)
                if tx.from_address == sender.get_offline_address():
                    self.local_ban_list.add(
                        sender.get_offline_address())
                    logger.info(
                        f"Add {sender.get_offline_address()} to blacklist for bad logs. New blacklist {self.local_ban_list}")
                    return False
        self.payment_log = combined_log
        return True

    def broadcast_logs(self):
        nodes_to_broadcast_to = int(len(self.neighbors) * p.broadcast_coverage)
        neighbors_to_broadcast = self.bc_random.choice(
            self.neighbors, nodes_to_broadcast_to, replace=False)
        for neighbor in neighbors_to_broadcast:
            neighbor.sync_logs(self.payment_log, self)
        return True

    def get_payment_log(self):
        return self.payment_log

    def has_payment(self, payment: OfflinePayment):
        if (payment in self.payment_log):
            return True
        for p in self.payment_log:
            if p.tx.id == payment.tx.id:
                return True
        return False

    def tick(self):
        if (not self.init_deposit):
            eo.add_event(UserEvent(self.check_online))
            self.init_deposit = True
        if (random.poisson(1/self.tx_rate)):
            eo.add_event(UserEvent(self.do_transaction))
