from modules.graph import Graph, nx, plt
from modules.user_node import UserNode


class BarabasiAlbert(Graph):
    def __init__(self, n=100, m=3,**attr):
        super().__init__(**attr)
        g = nx.barabasi_albert_graph(n, m, seed=self.seed)
        new_nodes = [(i,dict(data=UserNode(bc=self.bc, node_id=i, sim=self.sim,tx_rate=attr.get("tx_rate")))) for i in g.nodes]
        self.add_nodes_from(new_nodes)
        self.add_edges_from(g.edges)


if __name__ == '__main__':
    ba = BarabasiAlbert(100, 1)
    ba.draw()
    plt.show()
    ba.histogram()
