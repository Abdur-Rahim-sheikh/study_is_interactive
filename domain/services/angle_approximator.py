import math
from pathlib import Path

from PIL import Image

from ..models import Point


class AngleApproximator:
    """
    approximates angles and their points
    """

    def __init__(
        self,
        background_path="public/images/geometry_background",
        quadrant_split=4,
    ):
        if not (1 <= quadrant_split <= 4):
            raise ValueError("quadrant_split must be between 0 and 4, inclusive.")

        self.total_split = quadrant_split * 4

        self.background_path = Path(background_path)
        self.images = {}

    def __angle_preview(self, mode, graph_style=True):
        key = mode + "_graph" if graph_style else mode
        if key not in self.images:
            self.images[key] = Image.open(self.background_path / f"{key}.png")
        return self.images[key]

    def get_angle_preview(self, graph_style=True) -> Image:
        return self.__angle_preview("angle", graph_style=graph_style)

    def get_triangle_preview(self, graph_style=True) -> Image:
        return self.__angle_preview("triangle", graph_style=graph_style)

    def get_quadrangle_preview(self, graph_style=True) -> Image:
        return self.__angle_preview("quadrangle", graph_style=graph_style)

    def __signed_angle(self, a: Point, b: Point, c: Point) -> float:
        """
        The signed angle between the vectors BA and BC in radians.
        It calculates CBA angle
        """
        vec_a = (a.x - b.x, a.y - b.y)
        vec_b = (c.x - b.x, c.y - b.y)

        cross_product = vec_a[0] * vec_b[1] - vec_a[1] * vec_b[0]
        dot_product = vec_a[0] * vec_b[0] + vec_a[1] * vec_b[1]
        angle = math.atan2(cross_product, dot_product)
        return angle

    def get_approximated_angle(
        self, p1: Point, p2: Point, p3: Point, rad=True
    ) -> float:
        angle = self.__signed_angle(p1, p2, p3)
        if rad:
            block = 2 * math.pi / self.total_split
        else:
            block = 360 / self.total_split
            angle = math.degrees(angle)
        nearest = round(angle / block) * block
        return nearest

    def get_nearest_A(self, point1: Point, point2: Point, point3: Point) -> tuple:
        angle = self.__signed_angle(point1, point2, point3)
        nearest_angle = self.get_approximated_angle(point1, point2, point3)
        delta_rad = -nearest_angle + angle
        new_point1 = self.__rotate_point(point1, point2, delta_rad)

        return new_point1

    def __rotate_point(self, p: Point, center: Point, delta_rad: float) -> Point:
        x = p.x - center.x
        y = p.y - center.y

        dx = x * math.cos(delta_rad) - y * math.sin(delta_rad)
        dy = x * math.sin(delta_rad) + y * math.cos(delta_rad)

        # Translate back
        x_new = dx + center.x
        y_new = dy + center.y
        return Point(x_new, y_new)

    def normalize_bc_horizontally(self, a: Point, b: Point, c: Point) -> tuple:
        dx = c.x - b.x
        dy = c.y - b.y
        angle = math.atan2(dy, dx)  # radians

        a_rot = self.__rotate_point(a, b, -angle)
        c_rot = self.__rotate_point(c, b, -angle)

        if c_rot.x < b.x:
            b, c_rot = c_rot, b

            a_dx = a_rot.x - b.x
            a_rot = Point(b.x - a_dx, a_rot.y)

        return a_rot, b, c_rot

    def get_angle_points(
        self, a: Point, b: Point, c: Point, x_axis_parallel=False
    ) -> tuple:
        a, b, c = a.copy(), b.copy(), c.copy()

        a = self.get_nearest_A(a, b, c)
        if x_axis_parallel:
            a, b, c = self.normalize_bc_horizontally(a, b, c)

        return a, b, c

    def to_positive_degree(self, angle_rad: float) -> float:
        """
        Convert an angle in radians to a positive degree.
        """
        angle_degree = math.degrees(angle_rad)
        angle_degree = (angle_degree + 360) % 360
