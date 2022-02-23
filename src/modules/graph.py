import networkx as nx
import random as rd
import copy
import matplotlib.pyplot as plt
import math
import statistics


USER = "USER"
FRAUD_USER = "FRAUS_USER"
INTERMEDIARY = "INTERMEDIARY"
NETWORK ="NETWORK"

type_of_nodes = {

}

class Graph(nx.Graph):
    def __init__(self, **attr):
        super().__init__(**attr)
        self.seed = rd.randint(0, 1000) if "seed" not in attr.keys() else attr["seed"]
        self.attackdict = {
            "degree": nx.degree_centrality,
            "closeness": nx.closeness_centrality,
            "betweenness": nx.betweenness_centrality
        }
    

    def is_online(self):
        return self.has_connection_to_intermediary()
    
    def do_transaction(self):
        if (self.has_neightbor()):
            neighbor = self.get_random_neightbor()
            if (self.is_online()):
                self.do_transaction_to_node(neighbor)
            else:
                if (self.is_fradulent):
                    self.do_fradulent_offline_transaction_to_node(neighbor)
                else:
                    self.do_offline_transaction_to_node(neighbor)


    def get_largest_components_size(self):
        return len(max(nx.connected_components(self), key=len))

    def delete_random_nodes(self, n: int = 1, print_result=True):
        G = copy.deepcopy(self)
        rd.seed(self.seed)
        for i in range(n):
            node = rd.choice([i for i in nx.nodes(G)])
            if print_result:
                print("Removed node", node, "using", "random_fault")
            G.remove_node(node)
        return G

    def delete_node(self,node):
        G = copy.deepcopy(self)
        if node not in nx.nodes(G):
            print("Node not in the list of nodes")
            return
        G.remove_node(node)
        print(f"removed node {node}")
        return G

    def delete_nodes_attack(self, n: int = 1, centrality_index: str = "degree", print_result=True):
        #:TODO mekke pause og highlighte grafen så den lyser
        G = copy.deepcopy(self)
        rd.seed(self.seed)
        for i in range(n):
            analysis = self.attackdict[centrality_index](G)
            node = max(analysis, key=lambda key: analysis[key])
            if print_result:
                print("Removed node", node, "using", str(self.attackdict[centrality_index].__name__))
            G.remove_node(node)
        return G

    def get_shortest_path(self, node1, node2):
        path = None
        try:
            path = nx.shortest_path(self, node1, node2)
        except nx.NetworkXNoPath:
            pass
        return path

    def mark_nodes(self, mark_nodes):
        nodes = self.nodes()
        node_color = ["#1f78b4" if node not in mark_nodes else "#b82d2d" for node in nodes]
        self.draw(node_color=node_color)

    def mark_shortest_path(self, node1, node2):
        path = nx.shortest_path(self, node1, node2)
        edges = self.edges()
        marked_edges = [(element, path[i + 1]) for i, element in enumerate(path) if i < len(path) - 1]
        edge_color = [("k" if (u, v) not in marked_edges and (v, u) not in marked_edges else "#b82d2d") for u, v in
                      edges]
        nodes = self.nodes()
        node_color = ["#1f78b4" if node not in path else "#b82d2d" for node in nodes]
        self.draw(edge_color=edge_color, node_color=node_color)

    def draw(self, node_color="#1f78b4", edge_color="k", node_size=300):
        plt.figure(num=None, figsize=(10, 10))
        nx.draw_kamada_kawai(self, with_labels=True, edge_color=edge_color, node_color=node_color, node_size=node_size,
                             data=True)
