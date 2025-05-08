import math
from pathlib import Path

from PIL import Image

from domain.models import Point


class AngleApproximator:
    """
    A class to convert st_canvas which is from streamlit_drawable_canvas
    it changes dictionary to help feedback loop to initial drawing or others
    It supports conversion between point, line, rect and circle
    polygon does not return any json, so it's no use here
    """

    def __init__(
        self,
        background_path="public/images/geometry_background",
        quadrant_split=4,
        allowed_distance=2,
    ):
        if not (1 <= quadrant_split <= 4):
            raise ValueError("quadrant_split must be between 0 and 4, inclusive.")

        self.total_split = quadrant_split * 4
        self.allowed_distance = allowed_distance
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

    def __calculate_angle(self, a: Point, b: Point, c: Point, rad=False) -> float:
        """
        if rad is True, return angle in radians
        else return angle in degrees
        """
        BA = (a.x - b.x, a.y - b.y)
        BC = (c.x - b.x, c.y - b.y)

        dot_product = BA[0] * BC[0] + BA[1] * BC[1]
        magnitude_BA = (BA[0] ** 2 + BA[1] ** 2) ** 0.5
        magnitude_BC = (BC[0] ** 2 + BC[1] ** 2) ** 0.5
        angle = math.acos(dot_product / (magnitude_BA * magnitude_BC))
        if not rad:
            angle = math.degrees(angle)
        return angle

    def get_nearest_points(self, point1: Point, point2: Point, point3: Point) -> tuple:
        angle = self.__calculate_angle(point1, point2, point3)
        block = 360 / self.total_split
        nearest = round(angle / block) * block

        theta = math.radians(nearest)
        dx1 = point1.x - point2.x
        dx2 = point3.x - point2.x
        dy2 = point3.y - point2.y
        norm_BC = (dx2**2 + dy2**2) ** 0.5
        cos_theta = math.cos(theta)
        A = dy2
        B = dx1 * dx2
        C = norm_BC * cos_theta

        a = A**2 - C**2
        b = 2 * A * B
        c = B**2 - dx1**2 * C**2
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            raise ValueError("No real roots found")
        sqrt_discriminant = discriminant**0.5
        dy11 = (-b + sqrt_discriminant) / (2 * a)
        dy12 = (-b - sqrt_discriminant) / (2 * a)

        dy1 = min((dy11, dy12), key=lambda x: abs(x - point1.y))
        point1.y = dy1

        return point1

    def __rotate_point(self, p: Point, center: Point, angle_rad: float) -> Point:
        x = p.x - center.x
        y = p.y - center.y

        # Rotate
        x_new = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        y_new = x * math.sin(angle_rad) + y * math.cos(angle_rad)

        # Translate back
        return Point(x_new + center.x, y_new + center.y)

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
        self, a: Point, b: Point, c: Point, d: Point, x_axis_parallel=False
    ) -> tuple:
        f"""
        Raises:
            ValueError: if the distance between b and c is greater than {self.allowed_distance}
        """
        if b.distance_from(c) > 2:
            raise ValueError("সংযোগ বিন্দু অনেক দূরে")
        middle = Point((b.x + c.x) / 2, (b.y + c.y) / 2)
        a, b, c = a, middle, d
        a = self.get_nearest_points(a, b, c)
        if x_axis_parallel:
            a, b, c = self.normalize_bc_horizontally(a, b, c)

        return a, b, c


if __name__ == "__main__":
    approx = AngleApproximator()
    try:
        a = Point(0, 0)
        b = Point(0, 0)
        c = Point(3, 0)
        d = Point(1, 1)
        approx.get_angle_points(a, b, c, d)
        raise AssertionError(
            "Expected ValueError for too-far points, but none was raised."
        )
    except ValueError as e:
        assert "বিন্দু" in str(e), "Error message does not contain expected Bengali text."

    # 2. Return types: should return Point instances
    approx = AngleApproximator()
    a0, b0, c0 = Point(1, 2), Point(0, 0), Point(2, 0)
    d0 = Point(2, 2)
    a, b, c = approx.get_angle_points(a0, b0, c0, d0)
    assert isinstance(a, Point), "Expected 'a' to be a Point"
    assert isinstance(b, Point), "Expected 'b' to be a Point"
    assert isinstance(c, Point), "Expected 'c' to be a Point"

    # 3. x_axis_parallel alignment: BC should be horizontal
    approx = AngleApproximator()
    a0, b0, c0 = Point(1, 3), Point(0, 0), Point(2, 0)
    d0 = Point(3, 3)
    a, b, c = approx.get_angle_points(a0, b0, c0, d0, x_axis_parallel=True)
    assert abs(b.y - c.y) < 1e-6, (
        f"BC not horizontal after normalization: b.y={b.y}, c.y={c.y}"
    )

    # 4. Custom allowed_distance: no error when distance within limit
    approx = AngleApproximator(allowed_distance=5)
    a, b, c = approx.get_angle_points(
        Point(0, 0), Point(0, 0), Point(4, 0), Point(1, 1)
    )
    # If no exception was raised, test passes

    print("All tests passed.")
