import pytest

from domain.models import Point
from domain.services import AngleApproximator
import logging

logger = logging.getLogger(__name__)


def test_get_angle_points_distance_too_far_raises():
    # b and c distance is greater than allowed_distance (default 2)
    approximator = AngleApproximator()
    a = Point(0, 0)
    b = Point(0, 0)
    c = Point(3, 0)
    d = Point(1, 1)
    with pytest.raises(ValueError) as exc_info:
        approximator.get_angle_points(a, b, c, d)
    assert "দূরে" in str(exc_info.value)


def test_get_angle_points_returns_points():
    approximator = AngleApproximator()
    # Choose b and c at distance 2 (edge of allowed)
    a0 = Point(1, 2)
    b0 = Point(0, 0)
    c0 = Point(2, 0)
    d0 = Point(2, 2)
    a, b, c = approximator.get_angle_points(a0, b0, c0, d0)
    assert isinstance(a, Point)
    assert isinstance(b, Point)
    assert isinstance(c, Point)


def test_get_angle_points_x_axis_parallel_alignment():
    approximator = AngleApproximator()
    # Setup points such that x_axis_parallel=True will align BC horizontally
    a0 = Point(1, 3)
    b0 = Point(0, 0)
    c0 = Point(2, 0)
    d0 = Point(3, 3)
    a, b, c = approximator.get_angle_points(a0, b0, c0, d0, x_axis_parallel=True)
    # After normalization, BC should be horizontal: same y-coordinate
    assert pytest.approx(b.y, rel=1e-6) == pytest.approx(c.y, rel=1e-6)


def test_custom_allowed_distance():
    # Increase allowed_distance, should not raise
    approximator = AngleApproximator(allowed_distance=5)
    a = Point(0, 0)
    b = Point(0, 0)
    c = Point(4, 0)
    d = Point(1, 1)
    # Should not raise
    approximator.get_angle_points(a, b, c, d)


def test_middle_point():
    approximator = AngleApproximator()
    a = Point(1, 2)
    b = Point(0, 0)
    c = Point(2, 0)
    d = Point(2, 2)
    _, middle, _ = approximator.get_angle_points(a, b, c, d)
    assert isinstance(middle, Point)
    assert middle.x == 1
    assert middle.y == 0


@pytest.mark.parametrize(
    "a,b,c,d,expeted_a",
    [
        (
            Point(100, 100),
            Point(150, 150),
            Point(150, 150),
            Point(200, 150),
            Point(200, 100),
        ),
        (Point(0, 0), Point(1, 1), Point(1, 1), Point(2, 0), Point(0, 0)),
        (Point(-1, -1), Point(-2, -2), Point(-2, -2), Point(-3, -1), Point(-1, -1)),
    ],
)
def test_get_angle_points(a, b, c, d, expeted_a):
    approximator = AngleApproximator(quadrant_split=1)
    middle = Point((b.x + c.x) / 2, (b.y + c.y) / 2)
    a1, b1, c1 = approximator.get_angle_points(a, b, c, d)
    print(a, b, c)
    logger.debug(f"Angle points: {a}, {b}, {c}")
    assert a1 == expeted_a
    assert b1 == middle
    assert c1 == d
