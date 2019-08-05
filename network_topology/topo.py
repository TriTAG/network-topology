"""Module for creating a simplified graph from a set of linestrings."""

import logging
from .topology.strategy.factory import StrategyFactory

logger = logging.getLogger('network-topology')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)


class NetworkTopology(object):
    def __init__(self):
        pass


def getNetworkTopology(lineStrings,
                       thickness=14.0,
                       splitAtTeriminals=None,
                       turnThreshold=20.0,
                       minInnerPerimeter=200,
                       debugFolder=None):
    """Generate a bidirectional graph of the topology created by the lines."""
    sfactory = StrategyFactory(method='Skeleton')

    strategy = sfactory.getStrategy()

    topology = strategy.buildTopology(
        lineStrings=lineStrings,
        tolerance=thickness,
        splitAtEndpoints=splitAtTeriminals is not None)

    return topology._graph
