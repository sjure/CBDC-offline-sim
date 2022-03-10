from numpy.random import poisson, exponential
from modules.BaseNode import Node
from modules.Types import NETWORK
from Config import InputsConfig as p
class NetworkNode(Node):
    """ Network Node, the simulation of routers in the network"""
    is_online = True
    ticks_to_online = 0
    current_offline_ticks = 0
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
                self.ticks_to_online = exponential(p.network_recovery_rate)

        else:
            self.current_offline_ticks += 1
            if (self.current_offline_ticks >= self.ticks_to_online):
                self.is_online = True
                print("network online")
                self.current_offline_ticks = 0
                self.ticks_to_online = 0
