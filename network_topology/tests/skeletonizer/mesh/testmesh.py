"""Tests for Meshes."""
import unittest
# from mock import Mock, patch
import networkx as nx
import numpy as np
from shapely.geometry import Point
from network_topology.skeletonizer.mesh.mesh import Mesh
from network_topology.geometry.geomath import GeometryProcessor


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
        self.assertSequenceEqual(list(vertex), [0, 0])


class MeshSplitter(unittest.TestCase):
    """Tests for splitting long polygons."""

    def setUp(self):
        """Set up graph for test case."""

    def test_get_half(self):
        """Test splitting polygon into two by nodes."""
        mesh = Mesh([], [], nx.Graph())
        loop = {0: 1, 1: 2, 2: 3, 3: 0}
        half = mesh._getHalf(1, 3, loop)
        self.assertListEqual(half, [1, 2, 3])

    def test_get_half_adj(self):
        """Test splitting polygon into two by nodes."""
        mesh = Mesh([], [], nx.Graph())
        loop = {0: 1, 1: 2, 2: 3, 3: 0}
        half = mesh._getHalf(1, 0, loop)
        self.assertListEqual(half, [1, 2, 3, 0])

    def _diamondCase(self):
        graph = nx.Graph()
        graph.add_node(0, vertices=[0, 1, 2, 3, 4, 5])
        mesh = Mesh([[0, 0], [1, 0.5], [2, 1], [0, 2], [-1, 1.5], [-2, 1]],
                    [], graph)
        gp = GeometryProcessor()
        return mesh, gp

    def test_find_split_nodes(self):
        """Test correct nodes idenfied for splitting of polygon."""
        mesh, gp = self._diamondCase()
        top, bottom = mesh._findSplitNodes(0, 1, 0, gp)
        self.assertEqual(top, 0)
        self.assertEqual(bottom, 3)

    def test_split_poly(self):
        """Test polygon is split correctly."""
        mesh, _ = self._diamondCase()
        mesh._splitPoly(0, 0, 3)
        self.assertEqual(len(mesh._graph), 2)
        self.assertEqual(len(mesh._graph.edges), 1)

    def _diamondNeighboursCase(self):
        graph = nx.Graph()
        graph.add_node(0, vertices=[0, 1, 2, 3, 4, 5])
        graph.add_node(1, vertices=[0, 1, 6])
        graph.add_node(2, vertices=[1, 2, 7])
        graph.add_node(3, vertices=[0, 5, 8, 9])
        graph.add_edge(0, 1, common=(0, 1))
        graph.add_edge(0, 2, common=(1, 2))
        graph.add_edge(0, 3, common=(0, 5))
        mesh = Mesh([[0, 0], [1, 0.5], [2, 1], [0, 2], [-1, 1.5], [-2, 1],
                     [1, 0], [1.5, 1], [-2, 0], [-1, -2]],
                    [], graph)
        return mesh

    def test_split_shapes(self):
        """Test polygon is split correctly."""
        mesh = self._diamondNeighboursCase()
        mesh.splitShapes()
        self.assertEqual(len(mesh._graph[0]), 2)
        self.assertEqual(len(mesh._graph[4]), 3)

    def test_split_poly_neighbours(self):
        """Test polygon is split correctly."""
        mesh = self._diamondNeighboursCase()
        mesh._splitPoly(0, 0, 3)
        self.assertEqual(len(mesh._graph[0]), 3)
        self.assertEqual(len(mesh._graph[4]), 2)


class MeshMergeTest(unittest.TestCase):
    """Test case for internal elements."""

    def test_find_polygons_to_merge(self):
        """Test finding internal polygons."""
        graph = nx.Graph()
        graph.add_node(0, vertices=[0, 1, 2])
        graph.add_node(1, vertices=[0, 1, 3])
        graph.add_node(2, vertices=[1, 2, 4])
        graph.add_node(3, vertices=[0, 2, 5])
        graph.add_node(4, vertices=[1, 3, 6])
        graph.add_node(5, vertices=[0, 3, 7])
        graph.add_edge(0, 1, common=(0, 1))
        graph.add_edge(0, 2, common=(1, 2))
        graph.add_edge(0, 3, common=(0, 2))
        graph.add_edge(1, 4, common=(0, 3))
        graph.add_edge(1, 5, common=(1, 3))
        mesh = Mesh([[0, 0], [0, 2], [1, 1], [-1, 1],
                     [1, 2], [1, 0], [-1, 2], [-1, 0]],
                    [1, 1, 1, 1, 1, 1, 1, 1], graph)
        internal = mesh._findPolygonsToMerge()
        self.assertSequenceEqual(internal, [0, 1])


class MeshMidPointTest(unittest.TestCase):
    """Test case for finding midpoints in graph."""

    def setUp(self):
        """Set up graph."""
        graph = nx.Graph()
        graph.add_node(0, vertices=[0, 1, 3])
        graph.add_node(1, vertices=[1, 2, 3])
        graph.add_edge(0, 1, common=(1, 3))
        graph.add_edge(0, 3, common=(0, 3))
        self.mesh = Mesh([[0, 0], [0, 2], [2, 2], [1, 1]],
                         [1, 1, 1, 1], graph)

    def test_midpoints(self):
        """Test finding midpoints."""
        self.mesh._calculateMidPoints()
        self.assertEqual(Point(0.5, 0.5),
                         self.mesh._graph.edges[0, 3]['point'])


if __name__ == '__main__':
    unittest.main()
