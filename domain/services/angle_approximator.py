import math
from pathlib import Path

from PIL import Image

from domain.models import Point


class AngleApproximator:
    """
    approximates angles and their points
    """

    def __init__(
        self,
        background_path="public/images/geometry_background",
        quadrant_split=1,
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

    def get_approximated_angle(self, a: Point, b: Point, c: Point, rad=True) -> float:
        """
        The angle between the vectors BC to BA in degrees."""
        angle = self.__signed_angle(a, b, c)
        if rad:
            block = 2 * math.pi / self.total_split
        else:
            block = 360 / self.total_split
            angle = math.degrees(angle)

        nearest = round(angle / block) * block
        return nearest

    def get_nearest_A(self, point1: Point, point2: Point, point3: Point) -> tuple:
        nearest_angle = self.get_approximated_angle(point1, point2, point3)

        new_point1 = self.__rotate_point(point1, point2, -nearest_angle)

        return new_point1

    def __rotate_point(self, p: Point, center: Point, angle_rad: float) -> Point:
        x = p.x - center.x
        y = p.y - center.y

        current_angle = math.atan2(y, x)
        delta = angle_rad - current_angle
        dx = x * math.cos(delta) - y * math.sin(delta)
        dy = x * math.sin(delta) + y * math.cos(delta)

        # Translate back
        x_new = dx + center.x
        y_new = dy + center.y
        return Point(x_new, y_new)

    def normalize_bc_horizontally(self, a: Point, b: Point, c: Point) -> tuple:
        dx = c.x - b.x
        dy = c.y - b.y
        angle = math.atan2(dy, dx)  # radians

        a_rot = self.__rotate_point(a, b, -angle)
        b_rot = self.__rotate_point(b, b, -angle)
        c_rot = self.__rotate_point(c, b, -angle)

        if c_rot.x < b_rot.x:
            b_rot, c_rot = c_rot, b_rot

            a_dx = a_rot.x - b_rot.x
            a_rot = Point(b_rot.x - a_dx, a_rot.y)

        return a_rot, b_rot, c_rot

    def get_angle_points(
        self, a: Point, b: Point, c: Point, x_axis_parallel=False
    ) -> tuple:
        a, b, c = a.copy(), b.copy(), c.copy()

        a = self.get_nearest_A(a, b, c)
        if x_axis_parallel:
            a, b, c = self.normalize_bc_horizontally(a, b, c)

        return a, b, c
