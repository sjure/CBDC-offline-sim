import secrets
import json
import operator
import hashlib
import time
from modules.Blockchain import Transaction
from Config import InputsConfig as p


class UserBal():
    def __init__(self, balance, counter, prev_hash):
        self.balance = balance
        self.counter = counter
        self.prev_hash = prev_hash

    def __repr__(self):
        return json.dumps({
            "balance": self.balance,
            "counter": self.counter,
        })


class OfflinePayment():
    def __init__(self, tx, signature):
        self.tx = tx
        self.signature = signature
        self.ts = time.time_ns()
        self.hash = self.create_hash()

    def pm(self):
        """ Returns the payment object """
        tx = self.tx.transaction()
        return {
            "tx": tx,
            "signature": self.signature,
        }

    def create_hash(self):
        """ Returns the sha256 signature of the block """
        block_string = json.dumps(self.pm()).encode(
            'utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def __str__(self):
        tx = self.tx.transaction()
        payment = {
            "tx": tx,
            "signature": self.signature,
        }
        return json.dumps(payment)

    def __repr__(self):
        tx = self.tx.transaction()
        payment = {
            "tx": tx,
            "signature": self.signature,
        }
        return json.dumps(payment)

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self):
        return hash(self.hash)


class OfflineWallet():

    def __init__(self):
        """Initializes protected environment, generates a key-pair along with attestation"""
        self.balance = 0
        self.counter = 0
        self.account_id = secrets.token_hex(16)
        self.prev_hash = self.account_id
        self.certificate = None
        self.address_counter = {}
        self.__cert_init()

    def __cert_init(self):
        """Processes certifcate from the server; this is the second method that must be invoked,
        after which, other methods can be executed."""
        pass

    def _sign(self, transaction, prev_hash):
        # sign with private key of wallet
        return hashlib.sha256(transaction.hash.encode('utf-8') + prev_hash.encode('utf-8')).hexdigest()

    def deposit(self, tx, server_signature_of_deposit):
        """Converts online funds into offline funds, increases the offine balance."""
        # Validate server_signature_of_deposit
        self.balance += tx.amount
        op = OfflinePayment(
            tx, server_signature_of_deposit)
        return op

    def withdraw(self, reciever, amount):
        """Converts offline funds into online funds, decreases the offline balance."""
        self.counter += 1
        self.balance -= amount
        tx = Transaction(reciever, self.account_id,
                         amount, counter=self.counter)
        signature = self._sign(tx, self.prev_hash)
        op = OfflinePayment(tx, signature)
        self.prev_hash = tx.hash
        return op

    def pay(self, amount, reciever):
        """Creates an offine payment object."""
        self.counter += 1
        self.balance -= amount
        tx = Transaction(reciever, self.account_id,
                         amount, counter=self.counter)
        signature = self._sign(tx, self.prev_hash)
        op = OfflinePayment(tx, signature)
        self.prev_hash = tx.hash
        return op

    def collect(self, payment: OfflinePayment):
        """ Verifies an offline payment and applies it to the offline balance by increasing it with the
        payment amount. """
        # Check payment certificate is from sender
        # Check check signature with correct input
        if (payment.tx.from_address in self.address_counter):
            if (self.address_counter[payment.tx.from_address] >= payment.tx.counter):
                return False
        self.address_counter[payment.tx.from_address] = payment.tx.counter
        self.balance += payment.tx.amount
        return True

    def get_balance(self):
        """ Returns the current offline balance stored inside the TEE storage."""
        return self.balance


if __name__ == "__main__":
    ow = OfflineWallet()
    ow.deposit(100, "online-wallet", "")
    ow.pay(50, "A")
    print(ow.get_balance())
