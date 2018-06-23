"""Tests for EdgeIterator class."""
import unittest
from network_topology.skeletonizer.mesh.edgeiterator import EdgeIterator


class EdgeIterTestCase(unittest.TestCase):
    """Test of edge iterator."""

    def test_edge_iter(self):
        """Test that source,target are always expressed in ascending order."""
        ei = EdgeIterator([0, 1, 2])
        self.assertSequenceEqual(list(ei), [(0, 1), (1, 2), (0, 2)])

    def test_edge_iter_no_sort(self):
        """Test source,target are always expressed in order of appearance."""
        ei = EdgeIterator([0, 1, 2], sort=False)
        self.assertSequenceEqual(list(ei), [(0, 1), (1, 2), (2, 0)])
