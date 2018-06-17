"""Base class for topology creation strategies."""
from abc import ABCMeta, abstractmethod
import logging


class TopologyStrategy(object):
    """Abstract class for creating topologies."""

    __metaclass__ = ABCMeta

    def __init__(self):
        """Construct with logging capabilities."""
        self._logger = logging.getLogger('network-topology')

    @abstractmethod
    def buildTopology(self, lineStrings=[], tolerance=0):
        """Contstruct a topology out of the linestrings."""
