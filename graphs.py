import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

class ChatModel:
    def __init__(self):
        pass

    def generate(self, prompt):
        # This is a very simple implementation
        # In a real scenario, you'd want to use a more sophisticated model
        return f"Here's a simple response to your prompt: {prompt}"

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
