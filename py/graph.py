import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as pcolors
import networkx.algorithms.community as community
import numpy as np

try:
    from pyodide.http import open_url
except ModuleNotFoundError:
    def open_url(url):
        return url


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

        self.partition = None
        self.communities = None
        self.communities_colors = []

    def change_size(self, screen_size: tuple[int, int]):
        # change the axes value with the specific pixels size
        width, height = screen_size
        self.fig, self.axes = plt.subplots(figsize=(width / 100, height / 100))

    def __draw(self, g: nx.Graph, colors=None):
        if self.axes is None:
            self.change_size(ScreenSizes.S600P)  # default image size

        self.axes.set_position([0.005, 0.0, 0.98, 0.965])  # change the axes position to try to fill all image size
        self.axes.set_axis_off()
        plt.title(f'Graph with {g.number_of_nodes()} nodes')
        colors = colors if colors is not None else self.node_color
        return nx.draw_networkx(
            g,
            with_labels=self.has_labels,
            pos=self.position,
            ax=self.axes,
            node_size=self.node_size,
            node_color=colors,
            font_size=self.font_size,
            width=self.edge_width,
            arrowsize=self.arrow_size,
            edge_color=self.edge_color
        )

    def draw_subgraph(self):
        return self.__draw(self.subgraph)

    def draw_communities(self):
        return self.__draw(self.communities, self.communities_colors)

    def detect_communities(self, mat_color_map="tab20c"):
        communities = community.louvain_communities(self.subgraph.to_undirected())
        self.partition = {com: index for index, item in enumerate(communities) for com in item}

        nx.set_node_attributes(self.subgraph, self.partition, "community")
        self.communities = self.subgraph.subgraph(self.partition.keys())

        color_map = pcolors.ListedColormap(list(set(tuple(item) for item in np.random.rand(100, 3))))
        self.communities_colors = [color_map(self.partition[node]) for node in self.communities.nodes()]

        communities = [
            [node for node in self.partition.keys() if self.partition[node] == com]
            for com in set(self.partition.values())
        ]
        colors = [pcolors.rgb2hex(color_map(self.partition[nodes[0]])) for nodes in communities if nodes]

        return communities, colors


def load_graph(nodes: int):
    return Graph(open_url(
        'https://raw.githubusercontent.com/oliverTuesta/reddit-communities/main/soc-redditHyperlinks-title-5000.tsv'),
        'SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT', n_nodes=nodes)


