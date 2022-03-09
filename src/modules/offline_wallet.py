import secrets
import time

class OfflinePayment():
    def __init__(self, amount, sender, reciever, timestamp, counter, signature):
        self.amount = amount
        self.sender = sender
        self.reciever = reciever
        self.timestamp = timestamp
        self.counter = counter
        self.signature = signature


class OfflineWallet():
    payment_log = []
    def __init__(self):
        """Initializes protected environment, generates a key-pair along with attestation"""
        self.balance = 0
        self.counter = 0
        self.account_id = secrets.token_hex(16)
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
        self.counter += 1
        self.balance += amount
        signature = self._sign([amount,sender,self.account_id, int(time.time()*1e6), self.counter])
        return OfflinePayment(amount, sender, self.account_id, int(time.time()*1e6), self.counter, signature)


    def withdraw(self, reciever, amount):
        """Converts offline funds into online funds, decreases the offline balance."""
        self.counter += 1
        self.balance -= amount
        signature = self._sign([-amount, self.account_id, reciever, int(time.time()*1e6), self.counter])
        return OfflinePayment(-amount, self.account_id, reciever, int(time.time()*1e6), self.counter,signature)

    def pay(self, amount, reciever):
        """Creates an offine payment object."""
        self.counter += 1
        self.balance -= amount
        signature = self._sign([amount, self.account_id, reciever,int(time.time()*1e6), self.counter])
        return OfflinePayment(amount, self.account_id, reciever, int(time.time()*1e6), self.counter, signature)

    def collect(self, payment: OfflinePayment):
        """ Verifies an offline payment and applies it to the offline balance by increasing it with the
        payment amount. """
        if (payment in self.payment_log): raise Exception("Payment already in log")
        # Check time < 10 minutes from now
        # Check payment certificate is from sender
        # Check check signature with correct input
        self.balance += payment.amount
        self.payment_log.append(payment)

    def get_balance(self):
        """ Returns the current offline balance stored inside the TEE storage."""
        return self.balance

if __name__ == "__main__":
    ow = OfflineWallet()
    ow.deposit(100,"online-wallet","")
    ow.pay(50,"A")
    print(ow.get_balance())
    print(ow.payment_log)