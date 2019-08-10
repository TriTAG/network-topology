"""Tests for TopologyStrategy."""
import unittest
from mock import Mock
from network_topology.skeletonizer import SkeletonizingStrategy
from network_topology.skeletonizer.discrete.factory import DiscretizerFactory


class StrategyTestCase(unittest.TestCase):
    """Test case for SkeletonizingStrategy."""

    def setUp(self):
        """Set up graph for test case."""

    def test_skeletonize_strategy(self):
        """Test."""
        strategy = SkeletonizingStrategy(DiscretizerFactory(), Mock())
        strategy.buildTopology()
