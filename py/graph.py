import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyodide.http import open_url


class ScreenSizes:
    S600P = (800, 600)
    S720P = (1280, 720)
    S1080P = (1920, 1080)
    S1440P = (2560, 1440)
    S4K = (3840, 2160)


class Graph:
    def __init__(self, path: str, source: str, target: str, delimiter='\t', graphtype=nx.DiGraph(), n_nodes=None):
        # load the dataset
        self.dataset = pd.read_csv(path, delimiter=delimiter)
        # Create a directed graph from the dataset
        self.graph: nx.Graph = nx.from_pandas_edgelist(self.dataset, source=source, target=target, edge_attr=True,
                                                       create_using=graphtype)
        # set n_nodes and create a subgraph
        self.n_nodes = self.graph.number_of_nodes() if n_nodes is None else n_nodes
        self.subgraph = self.graph
        if self.n_nodes < self.graph.number_of_nodes():
            self.subgraph = self.graph.subgraph(list(self.graph.nodes)[:self.n_nodes])

        self.axes: plt.Axes = None  # axes for image size
        self.position = nx.spring_layout(self.subgraph)

        # properties
        self.edge_width = 0.5
        self.font_size = 10
        self.node_size = 70
        self.has_labels = True
        self.node_color = 'lightblue'
        self.edge_color = '#34444D'
        self.arrow_size = 5
        self.fig = None

    def change_size(self, screen_size: tuple[int, int]):
        # change the axes value with the specific pixels size
        width, height = screen_size
        self.fig, self.axes = plt.subplots(figsize=(width / 100, height / 100))

    def draw(self):
        if self.axes is None:
            self.change_size(ScreenSizes.S600P)  # default image size

        self.axes.set_position([0.005, 0.0, 0.98, 0.965])  # change the axes position to try to fill all image size
        self.axes.set_axis_off()
        plt.title(f'Graph with {self.n_nodes} nodes')
        return nx.draw_networkx(
            self.subgraph,
            with_labels=self.has_labels,
            pos=self.position,
            ax=self.axes,
            node_size=self.node_size,
            node_color=self.node_color,
            font_size=self.font_size,
            width=self.edge_width,
            arrowsize=self.arrow_size,
            edge_color=self.edge_color
        )  # draw the subgraph


def load_graph(nodes: int):
    return Graph(open_url(
        'https://raw.githubusercontent.com/oliverTuesta/reddit-communities/main/soc-redditHyperlinks-title-5000.tsv'),
        'SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT', n_nodes=nodes)
