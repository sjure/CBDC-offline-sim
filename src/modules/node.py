from abc import ABC, abstractmethod
import secrets
from modules.types import NETWORK, INTERMEDIARY,USER, FRAUD_USER
class Node(ABC):
    """ Node object to use in the graph """
    neighbors = []
    network_neighbors = []
    def __init__(self, graph=None, node_id=-1):
        self.graph = graph
        self.node_id = node_id
        self.account_id = secrets.token_hex(16)

    def init_neighbors(self):
        """
        Retrieves all neighbors in the network,
        puts network nodes in one list and transaction neighbors
        in another
        """
        network_neighbors = []
        neighbors = []
        for node_id in list(self.graph.neighbors(self.node_id)):
            if self.graph.get_node(node_id).type in [NETWORK, INTERMEDIARY]:
                network_neighbors.append(node_id)
            elif self.graph.get_node(node_id).type in [USER, FRAUD_USER]:
                neighbors.append(node_id)
            else:
                raise Exception("Neighbor type is not defined")
        self.network_neighbors = network_neighbors
        self.neighbors = neighbors

    @abstractmethod
    def tick(self) -> None:
        """ Tick funcktion to be called for each loop in the simulation"""
