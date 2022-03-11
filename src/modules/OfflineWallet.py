import secrets
import time
import operator
from modules.Blockchain import Transaction

class OfflinePayment():
    def __init__(self, tx, timestamp, counter, signature, certificate):
        self.tx = tx
        self.timestamp = timestamp
        self.counter = counter
        self.signature = signature
        self.certificate = certificate


class OfflineWallet():
    payment_log = []
    def __init__(self):
        """Initializes protected environment, generates a key-pair along with attestation"""
        self.balance = 0
        self.counter = 0
        self.account_id = secrets.token_hex(16)
        self.certificate = None
        self.__cert_init()

    def __cert_init(self):
        """Processes certifcate from the server; this is the second method that must be invoked,
        after which, other methods can be executed."""
        pass

    def _sign(self, transaction):
        # sign with private key of wallet
        return ""
    
    def deposit(self, amount, sender, server_signature_of_deposit):
        """Converts online funds into offline funds, increases the offine balance."""
        # Validate server_signature_of_deposit
        ts = int(time.time()*1e6)
        self.counter += 1
        self.balance += amount
        tx = Transaction(self.account_id, sender, amount, ts)
        signature = self._sign([amount,sender,self.account_id, ts, self.counter])
        return OfflinePayment(tx, ts, self.counter, signature, self.certificate)


    def withdraw(self, reciever, amount):
        """Converts offline funds into online funds, decreases the offline balance."""
        ts = int(time.time()*1e6)
        self.counter += 1
        self.balance -= amount
        tx = Transaction(reciever, self.account_id, amount, ts)
        signature = self._sign([-amount, self.account_id, reciever, ts, self.counter])
        return OfflinePayment(tx, ts, self.counter,signature, self.certificate)

    def pay(self, amount, reciever):
        """Creates an offine payment object."""
        ts = int(time.time()*1e6)
        self.counter += 1
        self.balance -= amount
        tx = Transaction(reciever, self.account_id, amount, ts)
        signature = self._sign([amount, self.account_id, reciever,ts, self.counter])
        return OfflinePayment(tx, ts, self.counter, signature, self.certificate)

    def collect(self, payment: OfflinePayment):
        """ Verifies an offline payment and applies it to the offline balance by increasing it with the
        payment amount. """
        if (payment in self.payment_log): raise Exception("Payment already in log")
        # Check time < 10 minutes from now
        # Check payment certificate is from sender
        # Check check signature with correct input
        self.balance += payment.tx.amount
        self.payment_log.append(payment)

    def get_balance(self):
        """ Returns the current offline balance stored inside the TEE storage."""
        return self.balance
    
    def redeem_payments(self):
        """ Returns payments to redeem to intermediary """
        payments_to_redeem = self.payment_log
        self.payment_log = []
        return payments_to_redeem

    def sync_payment_log(self, payment_log):
        for payment in payment_log:
            if payment not in self.payment_log:
                self.payment_log.append(payment)
        self.payment_log.sort(key=operator.attrgetter("timestamp"), reverse=False)

    def get_payment_log(self):
        return self.payment_log


if __name__ == "__main__":
    ow = OfflineWallet()
    ow.deposit(100,"online-wallet","")
    ow.pay(50,"A")
    print(ow.get_balance())
    print(ow.payment_log)
