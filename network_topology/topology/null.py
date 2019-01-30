"""Null class for topology."""

from abstract import AbstractTopology


class NullTopology(AbstractTopology):
    """Null implementation of as topology."""

    def addEdge(self, start, finish, lineString):
        """Add an edge to the topology."""

    def getEdge(self, start, finish, index):
        """Get the geometry for an edge."""

    def shortestPath(self, source, target):
        """Find path from source to target nodes."""

    def getNearbyEdges(self, point, tolerance):
        """Find candidate edges near the point."""
