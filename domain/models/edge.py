from dataclasses import dataclass

@dataclass
class Edge:
    source: str
    destination: str
    label: str = ""
    weight: int = 1

    

