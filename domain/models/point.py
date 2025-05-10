from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def distance_from(self, other: "Point") -> float:
        """Calculate the distance from this point to another point."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def copy(self) -> "Point":
        """Create a copy of this point."""
        return Point(self.x, self.y)
