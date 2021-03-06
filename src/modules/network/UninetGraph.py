import requests
from lxml import etree
from modules.network.BaseGraph import Graph, nx, plt

ONLINE = False
URL = "http://www.topology-zoo.org/files/Uninett2011.graphml"
PATH = "assets/graphs/uninet-2011.xml"


class UninetGraph(Graph):

    def __init__(self, **attr):
        super().__init__(**attr)
        if (ONLINE):
            XML_TO_PARSE = self.get_graph_from_url(URL)
        else:
            XML_TO_PARSE = self.get_graph_from_xml()
        tree = etree.XML(XML_TO_PARSE)
        graph = tree.find("{http://graphml.graphdrawing.org/xmlns}graph")
        nodes = graph.findall("{http://graphml.graphdrawing.org/xmlns}node")
        edges = graph.findall("{http://graphml.graphdrawing.org/xmlns}edge")
        self.graph_nodes = [{"id": n.attrib["id"], "label": n.getchildren(
        )[-1].text.replace(" ", "_")} for n in nodes]
        self.graph_edges = [(e.attrib["source"], e.attrib["target"])
                            for e in edges]
        self._init_nodes()
        self._init_edges()

    def _init_nodes(self):
        for node in self.graph_nodes:
            self.add_node(node["id"], label=node["label"])

    def _init_edges(self):
        self.add_edges_from(self.graph_edges)

    def get_graph_from_url(self, url):
        r = requests.get(url)
        return r.content

    def get_graph_from_xml(self):
        with open(PATH, "rb") as f:
            xml = f.read()
        return xml

    def draw(
            self,
            edge_color="#b4b4b4",
            node_color="k",
            figsize=(15, 14),
            with_labels=True,
            font_size=10,
            node_size=20,
            edge_width=0.6) -> None:

        plt.figure(num=None, figsize=figsize)
        if with_labels:
            labels = {n["id"]: n["label"] for n in self.graph_nodes}
        else:
            labels = None

        nx.draw_kamada_kawai(
            self,
            labels=labels,
            node_size=node_size,
            font_size=font_size,
            with_labels=with_labels,
            edge_color=edge_color,
            node_color=node_color,
            width=edge_width,
            linewidths=0,
            alpha=1
        )
        plt.show()


if __name__ == '__main__':
    rn = UninetGraph()
    print(rn.nodes())
    rn.draw()
