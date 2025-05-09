import pytest

from domain.models import Point
from domain.services import AngleApproximator


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
