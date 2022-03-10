from modules.BaseGraph import Graph, nx, plt
from modules.UserNode import UserNode
from Config import InputsConfig as p

class WattsStrogatz(Graph):
    """ Watts strgatz graph """
    def __init__(self, n, k, p, **attr):
        super().__init__(**attr)
        g = nx.watts_strogatz_graph(n, k, p, seed=self.seed)
        new_nodes = [(i,dict(data=UserNode(node_id=i, sim=self.sim,graph=self))) for i in g.nodes]
        self.add_nodes_from(new_nodes)
        self.add_edges_from(g.edges)
        self.init_neighbors()



if __name__ == '__main__':
    ba = WattsStrogatz(100, 2, 0.1)
    ba.draw()
    plt.show()
    ba.histogram()
    ba.mark_shortest_path(1, 98)
    print(ba.get_largest_components_size())
