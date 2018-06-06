import unittest
from mock import Mock
from network_topology.geometry.meshbuilder import MeshBuilder
from shapely.geometry import Polygon, MultiPolygon


class MeshBuilderTestCase(unittest.TestCase):
    def test_add_polygon(self):
        mb = MeshBuilder()
        mb._addRing = Mock()
        mb._addHole = Mock()
        mb.addShape(Polygon([[0, 0], [1, 1], [0, 1]]))
        mb._addRing.assert_called_once()
        mb._addHole.assert_not_called()

    def test_add_polygon_with_hole(self):
        mb = MeshBuilder()
        mb._addRing = Mock()
        mb._addHole = Mock()
        mb.addShape(
            Polygon([[0, 0], [1, 1], [0, 1]],
                    [[[0.25, 0.25], [0.75, 0.75], [0.25, 0.75]]]))
        mb._addRing.assert_called_once()
        mb._addHole.assert_called_once()

    def test_add_multi_polygon(self):
        mb = MeshBuilder()
        mb._addRing = Mock()
        mb.addShape(
            MultiPolygon([[[[0, 0], [1, 1], [0, 1]], []], [[[5, 5], [10, 10],
                                                            [10, 5]], []]]))
        self.assertEqual(mb._addRing.call_count, 2)
