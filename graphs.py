import sonnet
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

class Sonnet:
    def __init__(self):
        self.model = sonnet.ChatModel()

    def generate(self, prompt):
        return self.model.generate(prompt)

class D3Graph:
    def __init__(self):
        self.graph = Network(notebook=True, cdn_resources='remote')

    def add_node(self, node_id, label):
        self.graph.add_node(node_id, label=label)

    def add_edge(self, source, target):
        self.graph.add_edge(source, target)

    def show(self, filename='graph.html'):
        self.graph.show(filename)

class MatplotGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node_id, label):
        self.graph.add_node(node_id, label=label)

    def add_edge(self, source, target):
        self.graph.add_edge(source, target)

    def show(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, labels={node: data['label'] for node, data in self.graph.nodes(data=True)})
        plt.show()
