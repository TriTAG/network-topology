"""Tests for Mesh Skeletonization."""
import unittest
import networkx as nx
from network_topology.skeletonizer.mesh.mesh import Mesh


class GetEdgeTestCase(unittest.TestCase):
    """Test case for Meshes."""

    def setUp(self):
        graph = nx.Graph()
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        graph.add_edge(0, 5)
        graph.add_edge(5, 4)
        graph.add_edge(4, 6)
        graph.add_edge(6, 7)
        graph.add_edge(0, 8)
        self.mesh = Mesh([], [], graph)

    def _long_branch_test(self, start):
        nodes = self.mesh._getEdge(start)
        canon = range(5)
        if nodes[0] == 0:
            self.assertListEqual(list(canon), nodes)
        else:
            self.assertListEqual(list(reversed(canon)), nodes)

    def test_first_node_of_long(self):
        self._long_branch_test(1)

    def test_mid_node_of_long(self):
        self._long_branch_test(2)


class LoopGetEdgeTestCase(unittest.TestCase):
    """Test case for Meshes."""

    def setUp(self):
        graph = nx.Graph()
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        graph.add_edge(1, 4)
        self.mesh = Mesh([], [], graph)

    def test_loop(self):
        self.mesh._getEdge(3)


if __name__ == '__main__':
    unittest.main()
