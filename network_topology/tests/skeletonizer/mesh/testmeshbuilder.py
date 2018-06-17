import unittest
from mock import Mock
from network_topology.skeletonizer.mesh import Mesher
from shapely.geometry import Polygon, MultiPolygon, Point, LineString


class MesherTestCase(unittest.TestCase):
    def test_add_polygon(self):
        mb = Mesher()
        mb._addRing = Mock()
        mb._addHole = Mock()
        mb.addShape(Polygon([[0, 0], [1, 1], [0, 1]]))
        mb._addRing.assert_called_once()
        mb._addHole.assert_not_called()

    def test_add_polygon_with_hole(self):
        mb = Mesher()
        mb._addRing = Mock()
        mb._addHole = Mock()
        mb.addShape(
            Polygon([[0, 0], [1, 1], [0, 1]],
                    [[[0.25, 0.25], [0.75, 0.75], [0.25, 0.75]]]))
        mb._addRing.assert_called_once()
        mb._addHole.assert_called_once()

    def test_add_multi_polygon(self):
        mb = Mesher()
        mb._addRing = Mock()
        mb.addShape(
            MultiPolygon([[[[0, 0], [1, 1], [0, 1]], []], [[[5, 5], [10, 10],
                                                            [10, 5]], []]]))
        self.assertEqual(mb._addRing.call_count, 2)

    def test_add_ring(self):
        mb = Mesher()
        ring = Polygon([[0, 0], [1, 0], [1, 1]])
        mb._addRing(ring.exterior)
        self.assertEqual(len(mb._vertices), 3)
        self.assertEqual(len(mb._segments), 3)

    def test_add_hole(self):
        mb = Mesher()
        ring = Polygon([[0, 0], [1, 0], [1, 1]])
        mb._addHole(ring.exterior)
        self.assertEqual(len(mb._vertices), 3)
        self.assertEqual(len(mb._segments), 3)
        point = Point(mb._holes[-1])
        self.assertTrue(Polygon(ring).contains(point))

    def test_add_endpoints(self):
        mb = Mesher()
        lines = [LineString([[0, 0], [1, 1]]),
                 LineString([[0, 0], [0, 1]])]
        mb.addEndpoints(lines)
        self.assertEqual(len(mb._vertices), 3)

    def test_build_graph(self):
        mb = Mesher()
        polys = [[0, 1, 2], [1, 2, 3], [0, 2, 3]]
        graph = mb._buildGraph(polys)
        self.assertEqual(len(graph), 3)
        for i in range(3):
            self.assertEqual(len(graph[i]), 2)

    def test_discretize(self):
        pass
