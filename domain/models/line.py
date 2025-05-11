from dataclasses import dataclass
from .point import Point


@dataclass
class Line:
    start: Point
    end: Point
