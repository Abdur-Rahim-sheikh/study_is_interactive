from graphviz import Digraph, Graph
import streamlit as st
import time

class GraphVisualize:
    def __init__(self, graph: dict[list], graph_type:str="digraph", layout: str ="dot", node_shape: str = "box"):
        self.graph = Digraph(engine=layout)
        if graph_type == "graph":
            self.graph = Graph(engine=layout)

        for src, dest in graph.items():
            self.graph.node(src, shape=node_shape)
            for d in dest:
                self.graph.node(d, shape=node_shape)
                self.graph.edge(src, d)
       
        self.node_shape = node_shape

    def drawGraph(self, active_node, visited_nodes):
        graph = self.graph.copy()
        
        for node in visited_nodes:
            graph.node(node, shape=self.node_shape, style="filled", fillcolor="lightgreen")
        
        graph.node(active_node, shape=self.node_shape, style="filled", fillcolor="yellow")

        return graph
    
    def animate(self, path: list[tuple[str,str]], sleep_time: int = 1):
        if len(path) == 0:
            st.warning("No nodes to visualize.")
            return
        
        visited = []
        placeholder = st.empty()
        for node, info in path:
            graph = self.drawGraph(active_node=node, visited_nodes=visited)
            placeholder.graphviz_chart(graph)
            visited.append(node)
            if info:
                # info can also come in full blown md format
                st.toast(body=info, icon=":material/lightbulb:")
            time.sleep(sleep_time)

        st.success("Traversal complete!")