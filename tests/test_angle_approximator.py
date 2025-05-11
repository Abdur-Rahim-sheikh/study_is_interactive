import logging
import math

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
    "a,b,c,expected_a,quadrant_split",
    [
        (
            Point(x=291, y=113.0),
            Point(x=293, y=244.0),
            Point(x=446.0, y=243.0),
            Point(x=292.14370935960466, y=112.98753201950902),
            1,
        ),
        (
            Point(x=204, y=73),
            Point(x=290.5, y=241.0),
            Point(x=539, y=246.0),
            Point(x=294.3012623058589, y=52.07726339881148),
            1,
        ),
        (
            Point(x=204, y=73),
            Point(x=290.5, y=241.0),
            Point(x=539, y=246.0),
            Point(x=159.59935018252128, y=104.723553475438),
            2,
        ),
        (
            Point(x=204, y=73),
            Point(x=290.5, y=241.0),
            Point(x=539, y=246.0),
            Point(x=221.71430714774112, y=65.00347032161486),
            4,
        ),
        (
            Point(x=160.0, y=359),
            Point(x=291.0, y=243.0),
            Point(x=536.0, y=244.0),
            Point(x=116.02431615309038, y=242.28581353531877),
            1,
        ),
        (
            Point(x=160.0, y=359),
            Point(x=291.0, y=243.0),
            Point(x=536.0, y=244.0),
            Point(x=166.768501316889, y=366.22148649869547),
            2,
        ),
        (
            Point(x=160.0, y=359),
            Point(x=291.0, y=243.0),
            Point(x=536.0, y=244.0),
            Point(x=166.768501316889, y=366.22148649869547),
            4,
        ),
        (
            Point(x=402.0, y=339),
            Point(x=291.0, y=243.0),
            Point(x=538.0, y=244.0),
            Point(x=394.35040927445414, y=347.19065650432776),
            2,
        ),
    ],
)
def test_get_nearest_A(a, b, c, expected_a, quadrant_split):
    approximator = AngleApproximator(quadrant_split=quadrant_split)

    a1 = approximator.get_nearest_A(a, b, c)

    assert a1 == expected_a


@pytest.mark.parametrize(
    "point, center, angle, expected",
    [
        (Point(x=1, y=1), Point(x=0, y=0), math.pi / 2, Point(x=-1, y=1)),
    ],
)
def test_rotate_point(point, center, angle, expected):
    approximator = AngleApproximator()
    # rotated_point = approximator.__rotate_point(point, center, angle)
    rotated_point = approximator._AngleApproximator__rotate_point(point, center, angle)
    assert expected == rotated_point


@pytest.mark.parametrize(
    "a,b,c,expected_a,quadrant_split",
    [
        (
            Point(x=291, y=113.0),
            Point(x=293, y=244.0),
            Point(x=446.0, y=243.0),
            Point(x=292.14370935960466, y=112.98753201950902),
            1,
        ),
    ],
)
def test_get_angle_points_no_normalization(a, b, c, expected_a, quadrant_split):
    approximator = AngleApproximator(quadrant_split=quadrant_split)

    a1, b1, c1 = approximator.get_angle_points(a, b, c)
    assert b1 == b
    assert c1 == c
    assert expected_a == a1


@pytest.mark.parametrize(
    "a,b,c,quadrant_split",
    [
        (
            Point(x=291, y=113.0),
            Point(x=293, y=244.0),
            Point(x=446.0, y=243.0),
            1,
        ),
    ],
)
def test_get_angle_points_with_normalization(a, b, c, quadrant_split):
    approximator = AngleApproximator(quadrant_split=quadrant_split)

    a1, b1, c1 = approximator.get_angle_points(a, b, c, x_axis_parallel=True)

    angle = approximator._AngleApproximator__signed_angle(a, b, c)
    approximator_angle = approximator.get_approximated_angle(angle)

    angle2 = approximator._AngleApproximator__signed_angle(a1, b1, c1)

    assert b1.y == c1.y
    assert approximator_angle == angle2
