"""Module for strategy factory."""

from .null import NullStrategy
from ...skeletonizer import SkeletonizingStrategy

__all__ = ['StrategyFactory']


class StrategyFactory(object):
    """Factory for discretizers."""

    _methods = {'Skeleton': SkeletonizingStrategy}

    def __init__(self, method=None):
        """Constructor to set discretizing method."""
        if callable(method):
            self._cls = method
        else:
            self._cls = self._methods.get(method, NullStrategy)

    def getStrategy(self):
        """Return a new discretizer."""
        return self._cls()
