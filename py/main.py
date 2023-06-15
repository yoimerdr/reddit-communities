from py import load_graph, ScreenSizes
from js import addCommunities


def run_program(nodes: int, target="graph", image_size=ScreenSizes.S1080P):
    graph = load_graph(nodes)
    _, colors = graph.detect_communities()

    graph.change_size(image_size)
    graph.draw_communities()
    addCommunities(colors)
    return graph.fig
