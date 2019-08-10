"""Tests for GeometryProcessor class."""
import unittest
from network_topology.geometry.geomath import GeometryProcessor
from shapely.geometry import Polygon


class GeometryTestCase(unittest.TestCase):
    """Test of geometry processor."""

    def setUp(self):
        """Set up GeometryProcessor."""
        self._gp = GeometryProcessor()

    def test_square_moments(self):
        """Test area and moment are correctly calculated for a square."""
        poly = Polygon([[0, 0], [1, 0], [1, 1], [0, 1]])
        Mxx, Myy, Mxy = self._gp.centroidMoments(poly)
        self.assertAlmostEqual(Mxx, 1/12.)
        self.assertAlmostEqual(Myy, 1/12.)
        self.assertAlmostEqual(Mxy, 0)

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

    def test_diamond(self):
        """Test moments of inertia for a diamond."""
        poly = Polygon([[0, 0], [2, 1], [0, 2], [-2, 1]])
        Mxx, Myy, Mxy = self._gp.centroidMoments(poly)
        self.assertAlmostEqual(Mxx, 2/3.)
        self.assertAlmostEqual(Myy, 8/3.)
        self.assertAlmostEqual(Mxy, 0)

    def test_diamond_extra(self):
        """Test moments of inertia for a diamond."""
        poly = Polygon([[0, 0], [1, 0.5], [2, 1], [0, 2], [-1, 1.5], [-2, 1]])
        Mxx, Myy, Mxy = self._gp.centroidMoments(poly)
        self.assertAlmostEqual(Mxx, 2/3.)
        self.assertAlmostEqual(Myy, 8/3.)
        self.assertAlmostEqual(Mxy, 0)