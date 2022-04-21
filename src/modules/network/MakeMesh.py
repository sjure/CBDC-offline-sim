import networkx as nx
import logging
import math
from numpy import random
from Config import InputsConfig as p

logger = logging.getLogger("CBDCSimLog")

ROUTER_TIER_2_NODE_PREFIX = 1_000_000
ROUTER_TIER_1_NODE_PREFIX = 10_000_000_000

AVERAGE_ROUTERS_PER_NODE = p.average_routers_per_node
ROUTERS_TIER_2 = p.routers_tier_2


class SubNet():
    def __init__(self, graph, nodes, t1, t2):
        self.graph = graph
        self.nodes = nodes
        self.t1 = t1
        self.t2 = t2


def probabilistic_round(x):
    return int(math.floor(x + random.random()))


class MakeMesh():
    def __init__(self, prefix, n, m, **attr):
        self.prefix = prefix
        self.random_choice = random.RandomState(p.random_seed)
        subnet = self.make_mesh(n, m)
        self.t1 = subnet.t1[0]
        self.t2 = subnet.t2
        self.nodes = subnet.nodes
        self.graph = subnet.graph

    def make_mesh(self, n, m):
        prefix = self.prefix + "_"
        ba = nx.barabasi_albert_graph(n, m)
        ba_nodes = [prefix + str(i) for i in ba.nodes()]
        routers_tier_2 = [prefix + str(i) for i in range(
            ROUTER_TIER_2_NODE_PREFIX, ROUTER_TIER_2_NODE_PREFIX + ROUTERS_TIER_2)]
        routers_tier_1 = [prefix + str(ROUTER_TIER_1_NODE_PREFIX)]
        edges = []
        for node in range(n):
            selected_routers = self.random_choice.choice(range(ROUTERS_TIER_2), probabilistic_round(
                AVERAGE_ROUTERS_PER_NODE), replace=False)
            edges.extend([(node, ROUTER_TIER_2_NODE_PREFIX + router,)
                          for router in selected_routers])
        edges = edges + list(ba.edges())
        edges = [(prefix + str(i), prefix + str(j)) for i, j in edges]
        for router_2 in routers_tier_2:
            for router_1 in routers_tier_1:
                edges.append((router_2, router_1))

        graph = nx.Graph()
        graph.add_nodes_from(ba_nodes)
        graph.add_nodes_from(routers_tier_2)
        graph.add_nodes_from(routers_tier_1)
        graph.add_edges_from(edges)
        return SubNet(graph, ba_nodes, routers_tier_1, routers_tier_2)

    def get_graph(self):
        return self.graph
