from modules.node import Node
from modules.types import USER

class UserNode(Node):
    transactions = dict()
    type = USER
    def __init__(self):
        pass

    def do_transaction(self,node):
        pass

    def get_balance(self):
        pass

    def remove_from_balance(self):
        pass

    def add_to_balance(self):
        pass
    
