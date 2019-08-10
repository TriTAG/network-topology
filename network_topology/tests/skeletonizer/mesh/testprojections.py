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
        self.assertAlmostEqual(mesh._graph.node[1]['point'].y, 0.5,
                               delta=1e-6)
        self.assertGreaterEqual(mesh._graph.node[1]['point'].x, 0.5)
        self.assertLessEqual(mesh._graph.node[1]['point'].x, 1.0)

    def test_find_centroid_corner(self):
        graph = nx.Graph()
        graph.add_node(0, vertices=[0, 1, 2],
                       projections=[(1, Point(-1, 0)), (4, Point(0, 1))])
        graph.add_node(1, vertices=[1, 0, 3],
                       projections=[(0, Point(0.7071, 0.7071))])
        graph.add_node(4, vertices=[0, 2, 4],
                       projections=[(0, Point(0.7071, 0.7071))])
        graph.add_edge(0, 1, common=(0, 1), point=Point(0, 0.5))
        graph.add_edge(0, 4, common=(0, 2), point=Point(-0.5, 0))
        mesh = Mesh([[0, 0], [0, 1], [-1, 0], [1, 1], [0, -1]],
                    [], graph)
        mesh._calculateCentroids()
        self.assertAlmostEqual(mesh._graph.node[0]['point'], (-0.5, 0.5),
                               delta=0.0001)

    def test_midpoints_and_centroids_end_to_end(self):
        graph = nx.Graph()
        graph.add_node(0, vertices=[0, 1, 2])
        graph.add_node(1, vertices=[1, 0, 3])
        graph.add_node(2, vertices=[0, 3, 4])
        graph.add_node(3, vertices=[5, 3, 4])
        graph.add_node(4, vertices=[0, 2, 6])
        graph.add_node(5, vertices=[2, 6, 7])
        graph.add_node(6, vertices=[7, 6, 8])
        graph.add_edge(0, 1, common=(0, 1))
        graph.add_edge(1, 2, common=(0, 3))
        graph.add_edge(2, 3, common=(3, 4))
        graph.add_edge(0, 4, common=(0, 2))
        graph.add_edge(4, 5, common=(2, 6))
        graph.add_edge(5, 6, common=(6, 7))
        mesh = Mesh([[0, 0], [0, 1], [-1, 0], [1, 1], [1, 0],
                     [2, 1], [0, -1], [-1, -1], [0, -2]],
                    [], graph)
        mesh._calculateMidPoints()
        mesh._calculateProjections()
        mesh._calculateCentroids()

        self.assertAlmostEqual(mesh._graph.node[0]['point'], (-0.5, 0.5),
                               delta=0.0001)
        self.assertAlmostEqual(mesh._graph.node[1]['point'], (0, 0.5),
                               delta=0.01)
        self.assertAlmostEqual(mesh._graph.node[4]['point'], (-0.5, 0),
                               delta=0.01)
