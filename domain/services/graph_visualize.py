from graphviz import Source, Digraph, Graph
from ..models import Path
import streamlit as st
import time

class GraphVisualize:
    def __init__(self, graph: str, graph_type:str="digraph", layout: str ="dot", node_shape: str = "box"):
        self.graph = Digraph()
        if graph_type == "graph":
            self.graph = Graph()
        
        self.graph.body+= graph.splitlines()
        
        # self.graph.attr(layout=layout)
        self.node_shape = node_shape

    def drawGraph(self, active_node, visited_nodes, edges: list):
        graph = self.graph.copy()
        
        for node in visited_nodes:
            graph.node(node, shape=self.node_shape, style="filled", fillcolor="lightgreen")
        
        graph.node(active_node, shape=self.node_shape, style="filled", fillcolor="yellow")

        for edge in edges:
            graph.edge(edge.x, edge.y, label=edge.label)

        return graph
    
    def animate(self, path: Path, sleep_time: int = 1):
        edges = path.edges()
        visited = []
        placeholder = st.empty()

        for idx, step in enumerate(path.nodes):
            edges = path.edges(till=idx)
            graph = self.drawGraph(active_node=step, visited_nodes=visited, edges=edges)
            placeholder.graphviz_chart(graph)
            visited.append(step)
            time.sleep(sleep_time)

        st.success("Traversal complete!")