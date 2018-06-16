"""Tests for EdgeIterator class."""
import unittest
import math
from network_topology.geometry.geomath import GeometryProcessor
from shapely.geometry import Polygon


class GeometryTestCase(unittest.TestCase):
    """Test of geometry processor."""

    def setUp(self):
        """Set up GeometryProcessor."""
        self._gp = GeometryProcessor()

    def test_square_area(self):
        """Test area and moment are correctly calculated for a square."""
        poly = Polygon([[0, 0], [1, 0], [1, 1], [0, 1]])
        A, C, M = self._gp.areaCentroidMoments(poly)
        mxx = 1/12. + 0.25
        mxy = - 0.25
        self.assertEqual(A, 1)
        self.assertSequenceEqual(C, [0.5, 0.5])
        self.assertSequenceEqual(M, [mxx, mxx, mxy])

    def test_rect_axes_horiz(self):
        """Test principal axes for a horizontal rectangle."""
        poly = Polygon([[0, 0], [2, 0], [2, 1], [0, 1]])
        D, R = self._gp.principalAxis(poly)
        self.assertEqual(R, 2)
        self.assertSequenceEqual(D, (-1, 0))

    def test_rect_axes_vert(self):
        """Test principal axes for a vertical rectangle."""
        poly = Polygon([[0, 0], [1, 0], [1, 2], [0, 2]])
        D, R = self._gp.principalAxis(poly)
        self.assertEqual(R, 2)
        self.assertSequenceEqual(D, (0, -1))

    def test_rect_axes_45(self):
        """Test principal axes for a 45degree rectangle."""
        poly = Polygon([[0, 0], [-1, 1], [1, 3], [2, 2]])
        (dx, dy), R = self._gp.principalAxis(poly)
        self.assertEqual(R, 2)
        self.assertAlmostEqual(dx, dy)
