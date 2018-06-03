import unittest
from network_topology.geometry.edgeiterator import EdgeIterator


class EdgeIterTestCase(unittest.TestCase):
    def test_edge_iter(self):
        ei = EdgeIterator([0, 1, 2])
        self.assertSequenceEqual(list(ei), [(0, 1), (1, 2), (0, 2)])
