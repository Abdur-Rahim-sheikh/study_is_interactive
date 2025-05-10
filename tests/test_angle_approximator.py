import logging

import pytest

from domain.models import Point
from domain.services import AngleApproximator

logger = logging.getLogger(__name__)


def test_get_angle_points_returns_points():
    approximator = AngleApproximator()
    # Choose b and c at distance 2 (edge of allowed)
    a0 = Point(1, 2)
    b0 = Point(0, 0)
    c0 = Point(2, 0)
    a, b, c = approximator.get_angle_points(a0, b0, c0)
    assert isinstance(a, Point)
    assert isinstance(b, Point)
    assert isinstance(c, Point)


@pytest.mark.parametrize(
    "a,b,c,expected_degree,quadrant_split",
    [
        (Point(x=291, y=113.0), Point(x=293, y=244.0), Point(x=446.0, y=243.0), 90, 1),
        (Point(x=204, y=73), Point(x=290.5, y=241.0), Point(x=539, y=246.0), 90, 1),
        (Point(x=204, y=73), Point(x=290.5, y=241.0), Point(x=539, y=246.0), 135, 2),
        (Point(x=204, y=73), Point(x=290.5, y=241.0), Point(x=539, y=246.0), 112.5, 4),
        (
            Point(x=160.0, y=359),
            Point(x=291.0, y=243.0),
            Point(x=536.0, y=244.0),
            180,
            1,
        ),
        (
            Point(x=160.0, y=359),
            Point(x=291.0, y=243.0),
            Point(x=536.0, y=244.0),
            225,
            2,
        ),
        (
            Point(x=160.0, y=359),
            Point(x=291.0, y=243.0),
            Point(x=536.0, y=244.0),
            225,
            4,
        ),
        (
            Point(x=402.0, y=339),
            Point(x=291.0, y=243.0),
            Point(x=538.0, y=244.0),
            315,
            2,
        ),
    ],
)
def test_get_approximated_angle(a, b, c, expected_degree, quadrant_split):
    approximator = AngleApproximator(quadrant_split=quadrant_split)

    angle = approximator.get_approximated_angle(a, b, c)

    logger.debug(f"Angle points: {a}, {b}, {c}")
    assert pytest.approx(expected_degree, rel=1e-6) == angle


@pytest.mark.parametrize(
    "a,b,c,expected_a,quadrant_split",
    [
        (
            Point(x=291, y=113.0),
            Point(x=293, y=244.0),
            Point(x=446.0, y=243.0),
            Point(x=293, y=112.98478),
            1,
        ),
    ],
)
def test_get_angle_points(a, b, c, expected_a, quadrant_split):
    approximator = AngleApproximator(quadrant_split=quadrant_split)

    a1, b1, c1 = approximator.get_angle_points(a, b, c)

    logger.debug(f"Angle points: {a}, {b}, {c}, {b.distance_from(a)}")
    assert b1 == b
    assert c1 == c
    assert pytest.approx(expected_a, rel=1e-6) == a1
