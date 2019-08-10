"""Interface for discretizing geometery to get skeleton."""
from network_topology.skeletonizer.mesh.mesher import Mesher
from .null import NullDiscretizer

# __all__ = ['DiscretizerFactory']


class DiscretizerFactory(object):
    """Factory for discretizers."""

    _methods = {'Mesh': Mesher}

    def __init__(self, method=None):
        """Constructor to set discretizing method."""
        if callable(method):
            self._cls = method
        else:
            self._cls = self._methods.get(method, NullDiscretizer)

    def getDiscretizer(self):
        """Return a new discretizer."""
        return self._cls()
