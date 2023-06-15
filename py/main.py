from py import load_graph, ScreenSizes


def run_program(nodes: int, target="graph", image_size=ScreenSizes.S1080P):
    graph = load_graph(nodes)
    graph.change_size(image_size)
    graph.draw()
    return graph.fig
