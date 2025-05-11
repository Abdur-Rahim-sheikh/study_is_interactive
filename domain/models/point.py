import math
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def distance_from(self, other: "Point") -> float:
        """Calculate the distance from this point to another point."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def angle_to(self, other: "Point") -> float:
        """Calculate the signed angle from this point to another point."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.atan2(dy, dx)

    def copy(self) -> "Point":
        """Create a copy of this point."""
        return Point(self.x, self.y)

    def __eq__(self, other: "Point") -> bool:
        rel, abs_tol = 1e-6, 1e-9
        x_close = math.isclose(self.x, other.x, rel_tol=rel, abs_tol=abs_tol)
        y_close = math.isclose(self.y, other.y, rel_tol=rel, abs_tol=abs_tol)
        return x_close and y_close
