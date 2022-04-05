import secrets
import json
import operator
from modules.Blockchain import Transaction
from modules.wallets.OfflineWallet import OfflinePayment, OfflineWallet


class ManipulatedOfflineWallet(OfflineWallet):
    def __init__(self):
        """ Tampered wallet """
        super().__init__()

    def pay(self, amount, reciever):
        """Creates an offine payment object."""
        self.counter += 1
        #self.balance -= amount
        tx = Transaction(reciever, self.account_id,
                         amount, counter=self.counter)
        signature = self._sign(tx, self.prev_hash)
        op = OfflinePayment(tx, signature)
        self.prev_hash = tx.hash
        return op
