from numpy.random import random
from modules.BaseGraph import Graph, nx, plt
from modules.FraudUserNode import FraudUserNode
from modules.UserNode import UserNode
from modules.NetworkNode import NetworkNode
from modules.IntermediaryNode import IntermediaryNode
from Config import InputsConfig as p

def get_new_node(node_id,graph):
    if random() > p.fraud_node_percentage:
            return UserNode(node_id=node_id, graph=graph)
    else:
        return FraudUserNode(node_id=node_id, graph=graph)

class BarabasiAlbert(Graph):
    """ Barabasi albert graph """
    def __init__(self, n=100, m=3,**attr):
        super().__init__(**attr)
        g = nx.barabasi_albert_graph(n, m, seed=self.seed)
        new_nodes = [(i,dict(data=get_new_node(i,self))) for i in g.nodes]
        self.add_nodes_from(new_nodes)
        self.add_edges_from(g.edges)
        network_nodes = [(1000,dict(data=NetworkNode(node_id=1000,graph=self)))]
        self.add_edges_from([(i,1000) for i in list(self.nodes)])
        self.add_nodes_from(network_nodes)
        intermediary_nodes = [(2000,dict(data=IntermediaryNode(node_id=2000,graph=self)))]
        self.add_nodes_from(intermediary_nodes)
        self.add_edges_from([(2000,1000)])
        self.init_neighbors()


if __name__ == '__main__':
    ba = BarabasiAlbert(100, 1)
    ba.draw()
    plt.show()
    ba.histogram()
