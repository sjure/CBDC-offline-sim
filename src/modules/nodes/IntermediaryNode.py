""" The intermediary Node """
import operator
import logging
from numpy.random import poisson, exponential
from modules.nodes.BaseNode import Node
from modules.Types import INTERMEDIARY
from modules.Blockchain import BlockChain as bc
from Config import InputsConfig as p
from Statistics import Statistics
from EventOrganizer import EventOrganizer as eo
from modules.sort.SortPayments import sort_payments
logger = logging.getLogger("CBDCSimLog")

class IntermediaryNode(Node):
    """ Intermediary Node processes the blockchain """
    is_online = True
    ticks_to_online = 0
    current_offline_ticks = 0
    type = INTERMEDIARY
    fradulent_transactions = []

    def __init__(self, sim=None, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)

    def _sign(self,tx):
        signature = f"signed-transaction-{tx.id}-by-intermediary"
        return tx, signature

    def add_transaction_to_bc(self, from_account,to_account,amount):
        if (self.get_funds_of_node(from_account) < amount):
            logger.error(f"ERROR, not enough funds {from_account} {self.get_funds_of_node(from_account)}, {amount}")
            return False, None, ""
        if (amount <= 0):
            logger.error(f"ERROR, value less than zero {self.get_funds_of_node(from_account)}, {amount}")
            return False, None, ""
        tx_confirmed = bc.add_transaction(to_account, from_account, amount)
        tx, signature = self._sign(tx_confirmed)
        return True, tx, signature 

    def send_transaction(self, payer_node_id, payee_node_id, amount):
        payer_node = self.graph.get_node(payer_node_id)
        payee_node = self.graph.get_node(payee_node_id)
        Statistics.online_tx += 1
        Statistics.online_tx_volume += amount
        logger.info(f"Online transaction from {payer_node_id} to {payee_node_id} amount {amount}")
        return self.add_transaction_to_bc(payer_node.account_id,payee_node.account_id,amount)
    
    def is_valid_tx(self,account_id, amount):
        return self.get_funds_of_node(account_id) >= amount

    def offline_deposit(self, node, amount):
        logger.info(f"Depost to offline wallet from {node.account_id} to {node.get_offline_address()} amount {amount}")
        return self.add_transaction_to_bc(node.account_id,node.get_offline_address(),amount)

    def offline_withdraw(self, node, withdraw_payment):
        logger.info(f"Withdrawal from offline wallet from {withdraw_payment.tx.from_address} to {withdraw_payment.tx.to_address} amount {withdraw_payment.tx.amount}")
        # Verify signature of Secure hardware deletion of funds
        successfull_add = bc.add_transaction_from_offline(withdraw_payment.tx)
        if not successfull_add:
            logger.info(f"Withdrawal failed, Fradulent balance")
            self.fraud_payment_detected(withdraw_payment)

    def fraud_payment_detected(self,payment):
        tx = payment.tx
        if (tx not in self.fradulent_transactions):
            logger.error(f"ERROR: Fradulent payment logged amount={tx.amount} {tx.from_address}")
            self.fradulent_transactions.append(tx)
            if (tx.from_address not in Statistics.fraud_users.keys()):
                Statistics.fraud_users[tx.from_address] = tx.amount
            else:
                Statistics.fraud_users[tx.from_address] += tx.amount
            Statistics.fradulent_tx_detected += 1
            Statistics.fradulent_tx_detected_volume += tx.amount

            if p.intemediary_refund_payee_fradulent_transactions:
                # The payee does not loose money, and the bank is responsible
                # For getting the money back from the payer
                bc.deposit_money(tx.to_address,tx.amount)


    
    def redeem_payments(self, payments, node):
        if (len(payments)):
            logger.info(f"Redeem payemnts {node.get_offline_address()} {payments}")
            # topology sort
            payments = sort_payments(payments)
            for payment in payments:
                # Validate certificates
                # Validate payment with signature and certificate
                if not bc.has_transaction(payment.tx) and payment.tx not in self.fradulent_transactions:
                    successfull_add = bc.add_transaction_from_offline(payment.tx)
                    if not successfull_add:
                        self.fraud_payment_detected(payment)

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
