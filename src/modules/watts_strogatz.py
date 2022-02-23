from .graph import Graph, nx, plt
from modules.user_node import UserNode


class WattsStrogatz(Graph):
    def __init__(self, n, k, p, **attr):
        super().__init__(**attr)
        g = nx.watts_strogatz_graph(n, k, p, seed=self.seed)
        self.add_nodes_from(g.nodes, data=UserNode())
        self.add_edges_from(g.edges)


if __name__ == '__main__':
    ba = WattsStrogatz(100, 2, 0.1)
    ba.draw()
    plt.show()
    ba.histogram()
    ba.mark_shortest_path(1, 98)
    print(ba.get_largest_components_size())
