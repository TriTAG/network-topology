import unittest
import networkx as nx
from network_topology.skeletonizer.mesh.mesh import Mesh
from network_topology.geometry.point import Point


class ProjectionTestCase(unittest.TestCase):
    """Tests for the mesher."""

    def test_find_projection(self):
        graph = nx.Graph()
        graph.add_node(0, vertices=[0, 1, 2])
        graph.add_node(1, vertices=[1, 2, 3])
        graph.add_node(2, vertices=[1, 3, 4])
        # graph.add_node(3, vertices=[5, 3, 4])
        # graph.add_node(4, vertices=[5, 6, 4])
        graph.add_edge(0, 1, common=(1, 2), point=Point(0.5, 0.5))
        graph.add_edge(1, 2, common=(1, 3), point=Point(1, 0.5))
        # graph.add_edge(2, 3, common=(3, 4), point=Point(1.5, 0.5))
        # graph.add_edge(3, 4, common=(4, 5), point=Point(2, 0.5))
        mesh = Mesh([[0, 0], [1, 0], [0, 1], [1, 1], [2, 0], [2, 1], [3, 1]],
                    [], graph)
        mesh._calculateProjections()
        self.assertIn(mesh._graph.node[0]['projections'],
                      ([(1, (-1, 0))], [(1, (1, 0))]))
        self.assertIn(mesh._graph.node[2]['projections'],
                      ([(1, (-1, 0))], [(1, (1, 0))]))

    def test_find_centroid_simple(self):
        graph = nx.Graph()
        graph.add_node(0, vertices=[0, 1, 2], projections=[(1, Point(-1, 0))])
        graph.add_node(1, vertices=[1, 2, 3], projections=[(2, Point(-1, 0))])
        graph.add_node(2, vertices=[1, 3, 4], projections=[(1, Point(-1, 0))])
        graph.add_node(3, vertices=[5, 3, 4], projections=[(2, Point(-1, 0))])
        # graph.add_node(4, vertices=[5, 6, 4])
        graph.add_edge(0, 1, common=(1, 2), point=Point(0.5, 0.5))
        graph.add_edge(1, 2, common=(1, 3), point=Point(1, 0.5))
        graph.add_edge(2, 3, common=(3, 4), point=Point(1.5, 0.5))
        # graph.add_edge(3, 4, common=(4, 5), point=Point(2, 0.5))
        mesh = Mesh([[0, 0], [1, 0], [0, 1], [1, 1], [2, 0], [2, 1], [3, 1]],
                    [], graph)
        mesh._calculateCentroids()
        self.assertAlmostEqual(mesh._graph.node[1]['point'], (0.75, 0.5),
                               delta=0.01)

    def test_find_centroid_corner(self):
        graph = nx.Graph()
        graph.add_node(0, vertices=[0, 1, 2], projections=[(1, Point(-1, 0))])
        graph.add_node(1, vertices=[1, 2, 3], projections=[(2, Point(-1, 0))])
        graph.add_node(2, vertices=[1, 3, 4], projections=[(1, Point(-1, 0))])
        graph.add_node(3, vertices=[5, 3, 4], projections=[(2, Point(-1, 0))])
        # graph.add_node(4, vertices=[5, 6, 4])
        graph.add_edge(0, 1, common=(1, 2), point=Point(0.5, 0.5))
        graph.add_edge(1, 2, common=(1, 3), point=Point(1, 0.5))
        graph.add_edge(2, 3, common=(3, 4), point=Point(1.5, 0.5))
        # graph.add_edge(3, 4, common=(4, 5), point=Point(2, 0.5))
        mesh = Mesh([[0, 0], [1, 0], [0, 1], [1, 1], [2, 0], [2, 1], [3, 1]],
                    [], graph)
        mesh._calculateCentroids()
        self.assertAlmostEqual(mesh._graph.node[1]['point'], (0.75, 0.5), 
                               delta=0.01)