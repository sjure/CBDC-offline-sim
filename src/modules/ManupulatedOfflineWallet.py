import secrets
import time
import json
import operator
from modules.Blockchain import Transaction
from modules.OfflineWallet import OfflinePayment, OfflineWallet

class ManipulatedOfflineWallet(OfflineWallet):

    def pay(self, amount, reciever):
        """Creates an offine payment object."""
        ts = int(time.time()*1e6)
        # self.counter += 1
        # self.balance -= amount
        tx = Transaction(reciever, self.account_id, amount, ts)
        signature = self._sign([amount, self.account_id, reciever,ts, self.counter])
        return OfflinePayment(tx, ts, self.counter, signature, self.certificate)
