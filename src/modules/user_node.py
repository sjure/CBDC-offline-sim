from modules.node import Node
from modules.types import USER

class UserNode(Node):
    transactions = dict()
    type = USER
    def __init__(self):
        pass

    def do_transaction(self):
        pass
    
