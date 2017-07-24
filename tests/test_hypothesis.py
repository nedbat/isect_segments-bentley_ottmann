import math
import os.path
import sys
import unittest

from hypothesis import given
from hypothesis.strategies import builds, lists, integers, tuples

POLY_ISECT_MODULE_PATH = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(POLY_ISECT_MODULE_PATH)
import poly_point_isect


def collinear(p1, p2, p3):
    """Do three points lie on a line?"""
    # https://stackoverflow.com/questions/3813681/checking-to-see-if-3-points-are-on-the-same-line
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    if ((x1 <= x2 <= x3) or (x1 >= x2 >= x3)) and ((y1 <= y2 <= y3) or (y1 >= y2 >= y3)):
        return math.isclose((y1 - y2) * (x1 - x3), (y1 - y3) * (x1 - x2), abs_tol=1e-6)
    else:
        return False

nums = integers(min_value=-10000, max_value=10000)
points = tuples(nums, nums)
segments = builds(tuple, lists(points, min_size=2, max_size=2, unique=True))

class TheTest(unittest.TestCase):
    def assert_collinear(self, p1, p2, p3):
        self.assertTrue(collinear(p1, p2, p3))

    @given(lists(segments, min_size=2, max_size=100, unique=True))
    def test_intersections(self, segments):
        isects = poly_point_isect.isect_segments_include_segments(segments)
        for pt, segs in isects:
            for seg in segs:
                s1, s2 = seg
                self.assert_collinear(s1, pt, s2)
