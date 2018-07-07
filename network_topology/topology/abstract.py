"""Abstract class for topology."""

from abc import ABCMeta, abstractmethod


class AbstractTopology(object):
    """Interface for topology."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def addEdge(self, start, finish, lineString):
        """Add an edge to the topology."""

    @abstractmethod
    def getEdge(self, start, finish, index):
        """Get the geometry for an edge."""

    @abstractmethod
    def shortestPath(self, source, target):
        """Find path from source to target nodes."""

    @abstractmethod
    def getCandidateEdges(self, point, tolerance):
        """Find candidate edges near the point."""
