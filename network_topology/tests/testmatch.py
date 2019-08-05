import unittest
from network_topology import getMatchedRoutes
from shapely.geometry import LineString
import networkx as nx


class MatchTestCase(unittest.TestCase):
    def test_single_line(self):
        G = nx.MultiDiGraph()
        ls = LineString([[0, 0], [100, 0]])
        G.add_edge(1, 2, geom=ls, terminal=False)
        paths = getMatchedRoutes({'a': ls}, G)

        self.assertIn('a', paths, 'path not returned')
        self.assertEqual([(1, 2, 0)], paths['a'], 'incorrect path')

    def test_single_two_paths(self):
        G = nx.MultiDiGraph()
        ls1 = LineString([[0, 0], [100, 0]])
        ls2 = LineString([[0, 0], [100, 30]])
        G.add_edge(1, 2, geom=ls1, terminal=False)
        G.add_edge(1, 3, geom=ls2, terminal=False)
        paths = getMatchedRoutes({'a': ls1}, G)

        self.assertIn('a', paths, 'path not returned')
        self.assertEqual([(1, 2, 0)], paths['a'], 'incorrect path')

    def test_bidirectional(self):
        G = nx.MultiDiGraph()
        ls1 = LineString([[100, 0], [0, 0]])
        ls2 = LineString([[0, 0], [100, 0]])
        G.add_edge(1, 2, geom=ls1, terminal=False)
        G.add_edge(2, 1, geom=ls2, terminal=False)
        paths = getMatchedRoutes({'a': ls2}, G)
        self.assertIn('a', paths, 'path not returned')
        self.assertEqual([(2, 1, 0)], paths['a'], 'incorrect path')

    def test_path_correction(self):
        G = nx.MultiDiGraph()
        ls1 = LineString([[0, 0], [100, 0]])
        ls2 = LineString([[100, 0], [200, 0]])
        ls3 = LineString([[100, 0], [205, 0]])
        ls4 = LineString([[205, 0], [300, 0]])
        G.add_node(1, x=0, y=0)
        G.add_node(2, x=100, y=0)
        G.add_node(3, x=200, y=0)
        G.add_node(4, x=205, y=0)
        G.add_node(5, x=300, y=0)
        G.add_edge(1, 2, geom=ls1, terminal=False, length=100)
        G.add_edge(2, 3, geom=ls2, terminal=False, length=100)
        G.add_edge(2, 4, geom=ls3, terminal=False, length=100.125)
        G.add_edge(4, 5, geom=ls4, terminal=False, length=100.125)
        paths = getMatchedRoutes({'a': LineString([[0, 0], [300, 0]])}, G)

        self.assertIn('a', paths, 'path not returned')
        self.assertEqual([(1, 2, 0), (2, 4, 0), (4, 5, 0)], paths['a'],
                         'incorrect path')
