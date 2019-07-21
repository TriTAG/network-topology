"""Module for creating topologies from linestrings."""

from .topology import Topology
from .null import NullTopology

__all__ = ['TopologyFactory']


class TopologyFactory(object):
    """Factory for discretizers."""

    _methods = {'Topology': Topology}

    def __init__(self, method=None):
        """Constructor to set discretizing method."""
        if callable(method):
            self._cls = method
        else:
            self._cls = self._methods.get(method, NullTopology)

    def getToplogy(self):
        """Return a new discretizer."""
        return self._cls()
