"""Tests for EdgeIterator class."""
import unittest
from network_topology.skeletonizer.mesh.edgeiterator import EdgeIterator


class EdgeIterTestCase(unittest.TestCase):
    """Test of edge iterator."""

    def test_edge_iter(self):
        """Test that source,target are always expressed in ascending order."""
        ei = EdgeIterator([0, 1, 2])
        self.assertSequenceEqual(list(ei), [(0, 1), (1, 2), (0, 2)])
