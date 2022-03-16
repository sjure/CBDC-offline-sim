from numpy.random import random
from modules.network.BaseGraph import Graph, nx, plt
from modules.network.MakeMesh import MakeMesh
from modules.network.UninetGraph import UninetGraph
from modules.nodes.FraudUserNode import FraudUserNode
from modules.nodes.UserNode import UserNode
from modules.nodes.NetworkNode import NetworkNode
from modules.nodes.IntermediaryNode import IntermediaryNode
from Config import InputsConfig as p

def get_new_node(node_id,graph):
    if random() > p.fraud_node_percentage:
        return UserNode(node_id=node_id, graph=graph)
    else:
        return FraudUserNode(node_id=node_id, graph=graph)

def get_network_node(node_id,graph):
    if random() > p.fraud_node_percentage:
        return NetworkNode(node_id=node_id, graph=graph)
    else:
        return IntermediaryNode(node_id=node_id, graph=graph)

class NorGraph(Graph):
    t1_nodes = []
    t2_nodes = []
    user_nodes = []
    def __init__(self,**attr):
        super().__init__(**attr)
        un = UninetGraph()
        node_dict = {}
        for node in un.nodes():
            city = un.nodes[node]["label"]
            mesh = MakeMesh(city)
            new_nodes = [(i,dict(data=get_new_node(i,self))) for i in mesh.nodes]
            new_network_nodes = [(i,dict(data=get_network_node(i,self))) for i in mesh.t2]
            self.add_nodes_from(new_nodes)
            self.add_nodes_from(new_network_nodes)
            self.add_edges_from(mesh.graph.edges())
            node_dict[node] = mesh.t1
            self.t1_nodes.append(mesh.t1)
            self.t2_nodes = [*self.t2_nodes,*mesh.t2]
            self.user_nodes = [*self.user_nodes, *mesh.nodes]
        
        self.add_nodes_from([(node_dict[i],dict(data=get_network_node(node_dict[i],self))) for i in un.nodes()])
        self.add_edges_from([(node_dict[i],node_dict[j]) for i,j in un.edges()])

        self.init_neighbors()


if __name__ == "__main__":
    ng = NorGraph()
    print(ng.nodes())