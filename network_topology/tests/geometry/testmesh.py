import unittest
# from mock import Mock, patch
from network_topology.geometry.mesh import Mesh


class MeshTestCase(unittest.TestCase):
    def setUp(self):
        self.mesh = Mesh([[0, 0], [0, 2], [2, 2], [2, 0], [1, 1]],
                         [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 4, 0]],
                         [1, 1, 1, 1, 0])

    #     #self.patcher1 = patch('network_topology.geometry.buffer.logging')
    #     #self.loggerModule = self.patcher1.start()
    #     #self.bufferMaker = BufferMaker()

    # def tearDown(self):
    #     self.patcher1.stop()

    def test_internal_node(self):
        self.assertTrue(self.mesh.isInternal(4))

    def test_external_node(self):
        self.assertFalse(self.mesh.isInternal(0))

    def test_merge(self):
        self.mesh.mergePolygons([0, 1])
        polygons = [[0, 1, 2, 4], [], [2, 3, 4], [3, 4, 0]]
        for canon, candidate in zip(polygons, self.mesh.polygons()):
            self.assertSetEqual(set(canon), set(candidate))

    def test_full_merge(self):
        self.mesh.mergePolygons([0, 1, 2, 3])
        polygons = [[0, 1, 2, 3], [], [], []]
        for canon, candidate in zip(polygons, self.mesh.polygons()):
            self.assertSetEqual(set(canon), set(candidate))

    def test_get_vertex(self):
        vertex = self.mesh.getVertex(0)
        self.assertSequenceEqual(vertex, [0, 0])
