import secrets
import json
import operator
from modules.Blockchain import Transaction
from modules.OfflineWallet import OfflinePayment, OfflineWallet

class ManipulatedOfflineWallet(OfflineWallet):
    def __init__(self):
        """ Tampered wallet """
        super().__init__()

    def pay(self, amount, reciever):
        """Creates an offine payment object."""
        # self.counter += 1
        # self.balance -= amount
        tx = Transaction(reciever, self.account_id, amount)
        signature = self._sign([amount, self.account_id, reciever, self.counter])
        return OfflinePayment(tx, self.counter, signature)
