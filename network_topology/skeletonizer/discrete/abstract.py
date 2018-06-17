from abc import ABCMeta, abstractmethod
import logging


class AbsDiscretizer(object):
    """Interface for discretizing geometery to get skeleton."""

    __metaclass__ = ABCMeta

    def __init__(self):
        """Construct with logging capabilities."""
        self._logger = logging.getLogger('network-topology')

    @abstractmethod
    def discretize(self, tolerance):
        """Discretize the geometry, returns AbsDiscreteGeometry."""

    @abstractmethod
    def addShape(self, shape):
        """Add shape to be discretized."""

    @abstractmethod
    def addEndpoints(self, lineStrings):
        """Add endpoints of the linestrings to the representation."""


class AbsDiscreteGeometry(object):
    """Words."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def skeletonize(self):
        """Generate a SkeletonGraph of the geometry."""
