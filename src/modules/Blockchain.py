import hashlib
import secrets
import json
import time
import logging
logger = logging.getLogger("CBDCSimLog")


class Block():
    """ Block """

    def __init__(self, transactions, height, previous_block_hash):
        self.transactions = transactions
        self.height = height
        self.previous_block_hash = previous_block_hash
        self.block_hash = self.sign_block()

    def block(self):
        """ Returns the block object """
        return {
            "tx": [transaction.transaction() for transaction in self.transactions],
            "height": self.height,
            "prev_hash": self.previous_block_hash
        }

    def sign_block(self):
        """ Returns the sha256 signature of the block """
        block_string = json.dumps(self.block()).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def __str__(self):
        return json.dumps(self.block())

    def __repr__(self):
        return json.dumps(self.block())


class Transaction():
    """ Transaction """

    def __init__(self, to_address, from_address, amount):
        self.to_address = to_address
        self.from_address = from_address
        self.amount = amount
        self.nonce = secrets.token_hex(16)
        self.id = self.create_id()

    def transaction(self):
        """ Returns the transaction object """
        return {
            "to_address": self.to_address,
            "from_address": self.from_address,
            "amount": self.amount,
        }

    def create_id(self):
        """ Returns the sha256 signature of the block """
        block_string = json.dumps(self.transaction())
        transaction_string = (block_string + self.nonce).encode('utf-8')
        return hashlib.sha256(transaction_string).hexdigest()

    def __str__(self):
        return json.dumps(self.transaction())

    def __repr__(self):
        return json.dumps(self.transaction())


class BlockChain:
    """ Blockchain object """
    blocks = []
    queue = []
    iv = secrets.token_hex(16)

    def init_blockchain():
        """ Initializes the first block of the blockchain with the iv """
        new_block = Block(BlockChain.queue, len(
            BlockChain.blocks), BlockChain.iv)
        BlockChain.blocks.append(new_block)

    def check_trigger_new_block():
        """ Trigger new block if the queue is longer than the blocksize of queue """
        if len(BlockChain.queue) >= 10:
            BlockChain.add_block()

    def add_block():
        """ Add new block to the blockchain from the queue """
        if len(BlockChain.blocks) == 0:
            BlockChain.init_blockchain()
        else:
            new_block = Block(BlockChain.queue, len(
                BlockChain.blocks), BlockChain.blocks[-1].block_hash)
            BlockChain.blocks.append(new_block)
        BlockChain.queue = []

    def verify_block_chain():
        prev_hash = BlockChain.iv
        for block_height, block in enumerate(BlockChain.blocks):
            block_string = json.dumps(block.block()).encode('utf-8')
            hash = hashlib.sha256(block_string).hexdigest()
            if hash != block.block_hash:
                return False
            if block_height != 0:
                if block.previous_block_hash != prev_hash:
                    return False
            prev_hash = hash

        return True

    def balance_of(address):
        balance = 0
        for block in BlockChain.blocks:
            for transaction in block.transactions:
                if (transaction.to_address == address):
                    balance += transaction.amount
                if (transaction.from_address == address):
                    balance -= transaction.amount
        for transaction in BlockChain.queue:
            if (transaction.to_address == address):
                balance += transaction.amount
            if (transaction.from_address == address):
                balance -= transaction.amount
        return balance

    def is_valid_transaction(from_address, value):
        balance_of_sender = BlockChain.balance_of(from_address)
        return value <= balance_of_sender

    def add_transaction_from_offline(tx):
        is_valid = BlockChain.is_valid_transaction(tx.from_address, tx.amount)
        if not is_valid:
            logger.error(
                f"ERROR: Invalid offline transaction to_address={tx.to_address} from_address={tx.from_address} value={tx.amount}")
            return False
        BlockChain.queue.append(tx)
        BlockChain.check_trigger_new_block()
        return True

    def add_transaction(to_address, from_address, value):
        is_valid = BlockChain.is_valid_transaction(from_address, value)
        if not is_valid:
            logger.error(
                f"ERROR: Invalid transaction to_address={to_address} from_address={from_address} value={value}")
            return False
        tx = Transaction(to_address, from_address, value)
        BlockChain.queue.append(tx)
        BlockChain.check_trigger_new_block()
        return tx

    def deposit_money(address, value):
        tx = Transaction(address, "", value)
        BlockChain.queue.append(tx)
        BlockChain.check_trigger_new_block()

    def has_transaction(tx):
        id = tx.id
        for block in BlockChain.blocks:
            if tx in block.transactions:
                return True
        if tx in BlockChain.queue:
            return True
        return False

    def get_n_of_transactions():
        sum = 0
        for block in BlockChain.blocks:
            sum += len(block.transactions)
        return sum


if __name__ == "__main__":
    bc = BlockChain
    bc.deposit_money("sjur", 100)
    bc.add_transaction("dennis", "sjur", 1)
    bc.add_transaction("sjur", "sjur", 99)
    print(bc.blocks)
    print(bc.queue)
    print(bc.balance_of("dennis"))
    print(bc.balance_of("sjur"))
