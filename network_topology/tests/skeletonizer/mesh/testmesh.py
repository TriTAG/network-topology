"""Tests for Meshes."""
import unittest
# from mock import Mock, patch
import networkx as nx
from network_topology.skeletonizer.mesh.mesh import Mesh


class MeshTestCase(unittest.TestCase):
    """Test case for Meshes."""

    def setUp(self):
        """Set up graph for test case."""
        graph = nx.Graph()
        graph.add_node(0, vertices=[0, 1, 4])
        graph.add_node(1, vertices=[1, 2, 4])
        graph.add_node(2, vertices=[2, 3, 4])
        graph.add_node(3, vertices=[3, 4, 0])
        graph.add_edge(0, 1, common=(1, 4))
        graph.add_edge(0, 3, common=(0, 4))
        graph.add_edge(1, 2, common=(2, 4))
        graph.add_edge(2, 3, common=(1, 4))
        self.mesh = Mesh([[0, 0], [0, 2], [2, 2], [2, 0], [1, 1]],
                         [1, 1, 1, 1, 0], graph)
    #     #self.patcher1 = patch('network_topology.geometry.buffer.logging')
    #     #self.loggerModule = self.patcher1.start()
    #     #self.bufferMaker = BufferMaker()

    # def tearDown(self):
    #     self.patcher1.stop()

    def test_internal_node(self):
        """Test for internal node."""
        self.assertTrue(self.mesh._isInternal(4))

    def test_external_node(self):
        """Test for external node."""
        self.assertFalse(self.mesh._isInternal(0))

    def test_merge(self):
        """Test for merging two polygons."""
        self.mesh._mergeCluster([0, 1])
        polygons = [[0, 1, 2, 4], [2, 3, 4], [3, 4, 0]]
        for canon, candidate in zip(polygons, self.mesh.polygons()):
            self.assertSetEqual(set(canon), set(candidate))

    def test_full_merge(self):
        """Test mergining of all polygons."""
        self.mesh._mergeCluster([0, 1, 2, 3])
        polygons = [[0, 1, 2, 3]]
        for canon, candidate in zip(polygons, self.mesh.polygons()):
            self.assertSetEqual(set(canon), set(candidate))

    def test_collapse(self):
        """Test collapse of all polygons into one."""
        self.mesh.collapseShapes()
        polygons = [[0, 1, 2, 3]]
        for canon, candidate in zip(polygons, self.mesh.polygons()):
            self.assertSetEqual(set(canon), set(candidate))

    def test_polygons(self):
        """Test polygon iterator."""
        polygons = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 4, 0]]
        for canon, candidate in zip(polygons, list(self.mesh.polygons())):
            self.assertSetEqual(set(canon), set(candidate))

    def test_get_vertex(self):
        """Test probing vertex coordinates."""
        vertex = self.mesh.getVertex(0)
        self.assertSequenceEqual(vertex, [0, 0])
