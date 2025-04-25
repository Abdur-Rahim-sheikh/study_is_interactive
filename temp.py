from domain.services import GraphVisualize
from graphviz import Source
from domain.models import Path

graph_source = Source("""
    digraph G {
        "Is x < 0?" -> "Negative";
        "Is x < 0?" -> "Is x == 0?";
        "Is x == 0?" -> "Zero";
        "Is x == 0?" -> "Is x <= 1?";
        "Is x <= 1?" -> "Small Positive";
        "Is x <= 1?" -> "Large Positive";
    }
""")

path = Path(
    nodes=["Is x < 0?", "Negative"],
    descriptions=["Description"],
)

graph = GraphVisualize(graph=graph_source, layout="dot", node_shape="box")
graph.animate(path=path)