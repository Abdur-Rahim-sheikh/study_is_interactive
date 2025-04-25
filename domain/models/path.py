from dataclasses import dataclass

@dataclass
class Path:
    nodes: list
    descriptions: list

    def edges(self, till=None):
        if till is None:
            till = len(self.nodes)
        edges = []
        for i in range(till - 1):
            edges.append(Path(self.nodes[i], self.nodes[i + 1]))