from modules.node import Node
from modules.types import NETWORK

class NetworkNode(Node):
    """ Network Node, the simulation of routers in the network"""
    is_online = True
    type = NETWORK

    def __init__(self, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)

    def tick(self) -> None:
        """ The tick method of a router """
