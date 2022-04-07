import secrets
import json
import operator
from modules.Blockchain import Transaction
from modules.wallets.OfflineWallet import OfflinePayment, OfflineWallet


class ManipulatedOfflineWallet(OfflineWallet):
    active_fraud = False

    def __init__(self):
        """ Tampered wallet """
        super().__init__()

    def pay(self, amount, reciever):
        """Creates an offine payment object."""
        if (not self.active_fraud):
            return super().pay(amount, reciever)
        self.counter += 1
        #self.balance -= amount
        tx = Transaction(reciever, self.account_id,
                         amount, self.counter)
        signature = self._sign(tx, self.account_id)
        op = OfflinePayment(tx, signature)
        return op

    def reset(self, balance):
        self.active_fraud = True
        self.balance = balance
