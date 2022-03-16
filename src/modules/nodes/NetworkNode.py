import logging
from numpy.random import poisson, exponential
from modules.BaseNode import Node
from modules.Types import NETWORK
from Config import InputsConfig as p
from Statistics import Statistics
from EventOrganizer import EventOrganizer as eo
logger = logging.getLogger("CBDCSimLog")

class NetworkNode(Node):
    """ Network Node, the simulation of routers in the network"""
    is_online = True
    ticks_to_online = 0
    current_offline_ticks = 0
    type = NETWORK

    def __init__(self, node_id=-1,**attr):
        super().__init__(node_id=node_id, **attr)

    def handle_faults(self):
        if self.is_online:
            if (poisson(1/p.network_failure_rate)):
                self.is_online = False
                logger.info("network -> offline")
                self.ticks_to_online = int(exponential(p.network_recovery_rate))
                logger.info(f"{self.ticks_to_online} ticks to online")
                Statistics.network_failures += 1
        else:
            self.current_offline_ticks += 1
            if (self.current_offline_ticks >= self.ticks_to_online):
                logger.info("network -> online")
                self.is_online = True
                self.current_offline_ticks = 0
                self.ticks_to_online = 0
                Statistics.network_repairs += 1

    def tick(self) -> None:
        """ The tick method of a router """
        eo.add_event(self.handle_faults)
