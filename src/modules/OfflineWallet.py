import secrets
import json
import operator
import hashlib
from modules.Blockchain import Transaction
class OfflinePayment():
    def __init__(self, tx, counter, signature):
        self.tx = tx
        self.counter = counter
        self.signature = signature
        self.id = self.create_id()

    def pm(self):
        """ Returns the payment object """
        tx = self.tx.transaction()
        return {
            "tx":tx,
            "counter":self.counter,
        }
    
    def create_id(self):
        """ Returns the sha256 signature of the block """
        block_string = json.dumps(self.pm()).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def __str__(self):
        tx = self.tx.transaction()
        payment = {
            "tx":tx,
            "counter":self.counter,
        }
        return json.dumps(payment)

    def __repr__(self):
        tx = self.tx.transaction()
        payment = {
            "tx":tx,
            "counter":self.counter,
        }
        return json.dumps(payment)



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
        return 
    
    def deposit(self, tx, server_signature_of_deposit):
        """Converts online funds into offline funds, increases the offine balance."""
        # Validate server_signature_of_deposit
        self.counter += 1
        self.balance += tx.amount
        op = OfflinePayment(tx, self.counter, server_signature_of_deposit)
        self.payment_log.append(op)
        return op

    def withdraw(self, reciever, amount):
        """Converts offline funds into online funds, decreases the offline balance."""
        self.counter += 1
        self.balance -= amount
        tx = Transaction(self.account_id, reciever, amount)
        signature = self._sign([-amount, self.account_id, reciever, self.counter]) 
        op = OfflinePayment(tx, self.counter,signature)
        self.payment_log.append(op)
        return op

    def pay(self, amount, reciever):
        """Creates an offine payment object."""
        self.counter += 1
        self.balance -= amount
        tx = Transaction(reciever, self.account_id, amount)
        signature = self._sign([amount, self.account_id, reciever, self.counter])
        return OfflinePayment(tx, self.counter, signature)

    def collect(self, payment: OfflinePayment):
        """ Verifies an offline payment and applies it to the offline balance by increasing it with the
        payment amount. """
        if (payment in self.payment_log): raise Exception("Payment already in log")
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
            # Check payment with payment certificate
            if payment not in self.payment_log:
                self.payment_log.append(payment)

    def get_payment_log(self):
        return self.payment_log


if __name__ == "__main__":
    ow = OfflineWallet()
    ow.deposit(100,"online-wallet","")
    ow.pay(50,"A")
    print(ow.get_balance())
    print(ow.payment_log)
