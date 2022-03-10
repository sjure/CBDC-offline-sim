from numpy.random import poisson
from modules.BaseNode import Node
from modules.Types import NETWORK
from Config import InputsConfig as p
class NetworkNode(Node):
    """ Network Node, the simulation of routers in the network"""
    is_online = True
    type = NETWORK

    def __init__(self, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)

    def tick(self) -> None:
        """ The tick method of a router """
        if self.is_online:
            failure_rate = p.network_failure_rate
            if (poisson(1/failure_rate)):
                self.is_online = False
                print("network offline")
        else:
            if (poisson(1/p.network_recovery_rate)):
                self.is_online = True
                print("network online")


