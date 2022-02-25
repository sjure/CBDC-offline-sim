import hashlib
import secrets
import json

class Block():
    def __init__(self,transactions,height, previous_block_hash):
        self.transactions = transactions
        self.height = height
        self.previous_block_hash = previous_block_hash
        self.block_hash = self.sign_block()
    
    def block(self):
        return {
            "tx": self.transactions,
            "height":self.height,
            "prev_hash":self.previous_block_hash
        }

        
    def sign_block(self):
        block_string = json.dumps(self.block()).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()
        
    def __str__(self):
        return json.dumps(self.block())
            
    def __repr__(self):
        return json.dumps(self.block())


class BlockChain():
    def __init__(self):
        self.blocks = []
        self.queue = []
        self.iv = secrets.token_hex(16)

    def init_blockchain(self):
        new_block = Block(self.queue,len(self.blocks),self.iv)
        self.blocks.append(new_block)

    def check_trigger_new_block(self):
        if len(self.queue) >= 1:
            self.add_block()

    def add_block(self):
        if len(self.blocks) == 0:
            self.init_blockchain()
        else:
            new_block = Block(self.queue,len(self.blocks),self.blocks[-1].block_hash)
            self.blocks.append(new_block)
        self.queue = []
    
    def verify_block_chain(self):
        prev_hash = self.iv
        for block_height, block in enumerate(self.blocks):
            block_string = json.dumps(self.block()).encode('utf-8')
            hash = hashlib.sha256(block_string).hexdigest()
            if hash != block.block_hash:
                return False

            if block_height != 0:
                if block.previous_block_hash != prev_hash:
                    return False
            prev_hash = hash
            
        return True

    def balance_of(self, address):
        balance = 0
        for block in self.blocks:
            for transaction in block.transactions:
                if (transaction["to_address"] == address):
                    balance += transaction["value"]
                elif (transaction["from_address"] == address):
                    balance -= transaction["value"]
        return balance

    def is_valid_transaction(self,from_address,value):
        balance_of_sender = self.balance_of(from_address)
        return value <= balance_of_sender

    def add_transaction(self, to_address, from_address, value):
        is_valid = self.is_valid_transaction(from_address, value)
        if not is_valid:
            return False
        tx = {
            "to_address":to_address,
            "from_address":from_address,
            "value":value
        }
        self.queue.append(tx)
        self.check_trigger_new_block()
        return True
    
    def deposit_money(self,address,value):
        tx = {
            "to_address":address,
            "from_address":"",
            "value":value
        }
        self.queue.append(tx)
        self.check_trigger_new_block()

    def get_n_of_transactions(self):
        sum = 0
        for block in self.blocks:
            sum += len(block.transactions)
        return sum


if __name__ == "__main__":
    bc = BlockChain()
    bc.deposit_money("sjur", 100)
    bc.add_transaction("dennis","sjur",1)
    print(bc.blocks)
    print(bc.balance_of("dennis"))
    print(bc.balance_of("sjur"))