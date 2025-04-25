from dataclasses import dataclass

@dataclass
class Edge:
    x: str
    y: str
    label: str = ""