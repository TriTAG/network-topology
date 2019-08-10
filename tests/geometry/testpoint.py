"""Tests for Point class."""
import unittest
from network_topology.geometry.point import Point


class PointTestCase(unittest.TestCase):
    """Tests of Point."""

    def setUp(self):
        self.a = Point(1, 2)
        self.b = Point(-1, 3)
        self.t = (-1, 3)

    def test_args_constructor(self):
        p = Point(1, 2)
        self.assertEqual(p, (1, 2))

    def test_kwargs_constructor(self):
        p = Point(x=1, y=2)
        self.assertEqual(p, (1, 2))

    def test_add(self):
        self.assertEqual(self.a + self.b, (0, 5))

    def test_sub(self):
        self.assertEqual(self.a - self.b, (2, -1))

    def test_mul(self):
        self.assertEqual(self.a*2, (2, 4))

    def test_mul_order_switched(self):
        self.assertEqual(2*self.a, (2, 4))

    def test_add_tuple(self):
        self.assertEqual(self.a + self.t, (0, 5))

    def test_add_tuple_order_switched(self):
        self.assertEqual(self.t + self.a, (0, 5))

    def test_sub_tuple(self):
        self.assertEqual(self.a - self.t, (2, -1))

    def test_sub_tuple_order_switched(self):
        self.assertEqual(self.t - self.a, (-2, 1))

    def test_negative(self):
        self.assertEqual(-self.a, (-1, -2))

    def test_add_float(self):
        with self.assertRaises(TypeError):
            self.a + 5

    def test_sub_float(self):
        with self.assertRaises(TypeError):
            self.a - 5

    def test_mul_string(self):
        with self.assertRaises(TypeError):
            self.a * '5'

    def test_div(self):
        self.assertEqual(self.a/2, (.5, 1))

    def test_div_string(self):
        with self.assertRaises(TypeError):
            self.a / '5'

    def test_abs(self):
        self.assertEqual(abs(Point(3, 4)), 5)
