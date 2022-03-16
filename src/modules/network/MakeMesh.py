import networkx as nx
import logging
logger = logging.getLogger("CBDCSimLog")

ROUTER_TIER_2_NODE_PREFIX = 1_000_000
ROUTER_TIER_1_NODE_PREFIX = 1_000_000_000

NODES = 100
AVERAGE_ROUTERS_PER_NODE = 1.5
ROUTERS_TIER_2 = 3

class SubNet():
    def __init__(self,graph,nodes,t1,t2):
        self.graph = graph
        self.nodes = nodes
        self.t1 = t1
        self.t2 = t2

class MakeMesh():
    def __init__(self,prefix):
        self.prefix = prefix
        subnet = self.make_mesh()
        self.t1 = subnet.t1[0]
        self.t2 = subnet.t2
        self.nodes = subnet.nodes
        self.graph = subnet.graph

    def make_mesh(self):
        prefix = self.prefix + "_"
        ba = nx.barabasi_albert_graph(NODES,3)
        ba_nodes = [prefix + str(i) for i in ba.nodes()]
        routers_tier_2 = [prefix + str(i) for i in range(ROUTER_TIER_2_NODE_PREFIX,ROUTER_TIER_2_NODE_PREFIX + ROUTERS_TIER_2)]
        routers_tier_1 = [prefix + str(ROUTER_TIER_1_NODE_PREFIX)]
        nodes_per_partition = int(NODES*AVERAGE_ROUTERS_PER_NODE/ROUTERS_TIER_2)
        logger.info(f"Nodes per partition {nodes_per_partition}")
        partitions = []
        for i in range(ROUTERS_TIER_2):
            if (i ==0):
                range_start=0
                range_end =range_start + nodes_per_partition
            elif (i== ROUTERS_TIER_2-1):
                range_end=NODES-1
                range_start = range_end-nodes_per_partition
            else:
                range_start = int((i*0.5)*nodes_per_partition)
                range_end= int((i*1.5)*nodes_per_partition)
                range_start = range_start-int(nodes_per_partition/2)
                range_end = range_end+int(nodes_per_partition/2)
            range_start = max(min(range_start,NODES-1),0)
            range_end = min(range_end,NODES-1)
            partitions.append((range_start,range_end))
        logger.info(f"Network partitions {partitions}")
        edges =[]
        for router_index, part in enumerate(partitions):
            node_id_start, node_id_end = part
            for node_id in range(node_id_start,node_id_end+1):
                edges.append((ROUTER_TIER_2_NODE_PREFIX + router_index,node_id))

        edges = edges + list(ba.edges())
        edges = [(prefix + str(i), prefix + str(j)) for i,j in edges]
        for router_2 in routers_tier_2:
            for router_1 in routers_tier_1:
                edges.append((router_2,router_1))

        graph = nx.Graph()
        graph.add_nodes_from(ba_nodes)
        graph.add_nodes_from(routers_tier_2)
        graph.add_nodes_from(routers_tier_1)
        graph.add_edges_from(edges)
        return SubNet(graph,ba_nodes,routers_tier_1, routers_tier_2)
    
    def get_graph(self):
        return self.graph