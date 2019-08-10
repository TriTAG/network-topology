"""Interface for discretizing geometry to make a skeleton."""

from abc import ABCMeta, abstractmethod
import logging


class AbsDiscreteGeometry(object):
    """Words."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def skeletonize(self, splitAtEndpoints, topology):
        """Generate a SkeletonGraph of the geometry."""
