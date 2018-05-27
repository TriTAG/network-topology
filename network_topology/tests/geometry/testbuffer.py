import unittest
from mock import Mock, patch
from network_topology.geometry.buffer import BufferMaker
from shapely.geometry import LineString, Point, Polygon, MultiPolygon

class BufferTestCase(unittest.TestCase):
    def setUp(self):
        self.patcher1 = patch('network_topology.geometry.buffer.logging')
        self.loggerModule = self.patcher1.start()
        self.bufferMaker = BufferMaker()

    def tearDown(self):
        self.patcher1.stop()

    def test_buffer_point(self):
        shapes = [Point(0, 0)]
        bufferedShapes = self.bufferMaker._bufferShapes(shapes, thickness=10)
        diff = abs(bufferedShapes[0].area - 78.5398)/78.5398  # 5**2 pi
        self.assertLess(diff, 0.1)

    def test_buffer_line(self):
        shapes = [LineString([[0, 0], [100, 0]])]
        bufferedShapes = self.bufferMaker._bufferShapes(shapes, thickness=10)
        diff = abs(bufferedShapes[0].area - 1078.5398)/1078.5398
        self.assertLess(diff, 0.01)

    def test_remove_holes_polygon(self):
        bigShape = Polygon([[0, 0], [100, 0], [100, 100], [0, 100]],
                           [[[10, 10], [20, 10], [20, 20], [10, 20]],
                            [[90, 90], [90, 85], [85, 85], [85, 90]]])
        filledShape = self.bufferMaker._removeHoles(bigShape,
                                                    minInnerPerimeter=21)
        self.assertEqual(len(filledShape.interiors), 1)

    def test_remove_holes_multipolygon(self):
        bigShape = MultiPolygon([([[0, 0], [100, 0], [100, 100], [0, 100]],
                                  [[[10, 10], [20, 10], [20, 20], [10, 20]]]),
                                 ([[200, 0], [300, 0], [300, 100], [200, 100]],
                                  [[[210, 10], [215, 10], [215, 15], [210, 15]]])])
        filledShape = self.bufferMaker._removeHoles(bigShape,
                                                    minInnerPerimeter=21)
        self.assertEqual(len(filledShape.geoms), 2)
        self.assertEqual(len(filledShape.geoms[0].interiors), 1)
        self.assertEqual(len(filledShape.geoms[1].interiors), 0)

    def test_buffer_end_to_end(self):
        ls = [LineString([[0, 0], [100, 0]]),
              LineString([[10, 10], [10, -30]]),
              LineString([[20, 10], [20, -30]]),
              LineString([[0, -10], [100, -10]]),
              LineString([[40, 10], [40, -30]])]
        bufferedShape = self.bufferMaker.makeBufferedShape(ls, 5, 25)
        self.assertEqual(len(bufferedShape.interiors), 1)
