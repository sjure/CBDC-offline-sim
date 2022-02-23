from modules.graph import Graph, nx, plt
from modules.user_node import UserNode


class BarabasiAlbert(Graph):
    def __init__(self, n, m, **attr):
        super().__init__(**attr)
        g = nx.barabasi_albert_graph(n, m, seed=self.seed)
        self.add_nodes_from(g.nodes, data=UserNode())
        self.add_edges_from(g.edges)


if __name__ == '__main__':
    ba = BarabasiAlbert(100, 1)
    ba.draw()
    plt.show()
    ba.histogram()
