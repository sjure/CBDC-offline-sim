from modules.node import Node
from modules.types import NETWORK
import secrets
from numpy import random

class NetworkNode(Node):
        is_online = True
        type = NETWORK

        def __init__(self, node_id=-1,**attr):
            super().__init__(node_id=node_id, **attr)

        def tick(self):
            pass
        