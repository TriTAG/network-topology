"""Null class for topology strategy."""

from .abstract import TopologyStrategy

class NullStrategy(TopologyStrategy):
    def buildTopology(self, lineStrings=[], tolerance=0,
                      splitAtEndpoints=True):
        """Contstruct a topology out of the linestrings."""