"""Tests for Topology class."""
import unittest
from network_topology.topology.topology import Topology
from shapely.geometry import LineString, Point
import networkx as nx
import math


class TopologyTestCase(unittest.TestCase):
    """Test of topology."""

    def test_path(self):
        """Test finding the shortest path."""
        graph = nx.MultiDiGraph()
        nodes = [Point(0, 0), Point(1, 1), Point(1, 2), Point(0, 2),
                 Point(1, 0)]
        for u, v in [[0, 1], [0, 3], [1, 2],  [3, 2], [0, 4], [4, 1]]:
            graph.add_edge(u, v, geom=LineString([nodes[u], nodes[v]]))
            graph.add_edge(v, u, geom=LineString([nodes[v], nodes[u]]))
        topo = Topology(graph=graph, nodes=nodes)
        edges, distances = topo.shortestPath(0, 2)
        self.assertSequenceEqual(edges, [(0, 1, 0), (1, 2, 0)])
        self.assertSequenceEqual(distances, [math.sqrt(2), 1])

    def test_no_path(self):
        """Test if no path can be found between source and destination."""
        graph = nx.MultiDiGraph()
        nodes = [Point(0, 0), Point(1, 1)]
        graph.add_node(0)
        graph.add_node(1)
        topo = Topology(graph=graph, nodes=nodes)
        edges, distances = topo.shortestPath(0, 1)
        self.assertSequenceEqual(edges, [])
        self.assertSequenceEqual(distances, [float('inf')])

    def test_add_edge(self):
        """Test adding an edge."""
        topo = Topology()
        topo.addEdge(LineString([[0, 0], [1, 1], [1, 2]]))
        topo.addEdge(LineString([[2, 2], [1, 2]]))
        self.assertEqual(len(topo._graph.nodes), 3)

    def test_get_edge(self):
        """Test retrieving an edge."""
        graph = nx.MultiDiGraph()
        graph.add_edge(0, 1, geom=LineString([[0, 0], [0, 1]]))
        topo = Topology(graph=graph)
        self.assertEqual(topo.getEdge(0, 1, 0).length, 1)

    def test_get_candidates(self):
        """Test getting candidate segments near a point."""
        topo = Topology()
        topo.addEdge(LineString([[0, 0], [1, 1], [1, 2]]))
        topo.addEdge(LineString([[2, 2], [1, 2]]))
        candidates = topo.getCandidateEdges(Point(1, 1), 0.1)
        self.assertSetEqual(set(candidates), {(0, 1, 0), (1, 0, 0)})
