"""Module for skeletonizing strategy to create topologies."""

from network_topology.topology.strategy import TopologyStrategy
from network_topology.geometry.buffer import BufferMaker
from network_topology.topology import TopologyFactory


class SkeletonizingStrategy(TopologyStrategy):
    """Class for creating a topology using a skeletonizing strategy."""

    def __init__(self, discretizerFactory, bufferMaker=None,
                 topologyFactory=None):
        """Constructor for skeletonizing strategy."""
        self._discretizerFactory = discretizerFactory
        self._bufferMaker = bufferMaker or BufferMaker()
        self._topologyFactory = topologyFactory or TopologyFactory(method='Topology')
        super(SkeletonizingStrategy, self).__init__()

    def buildTopology(self, lineStrings=[], tolerance=0,
                      splitAtEndpoints=True):
        """Contstruct a topology out of the linestrings."""
        shape = self._bufferMaker.makeBufferedShape(
            lineStrings,
            thickness=tolerance,
            minInnerPerimeter=tolerance * tolerance)
        discretizer = self._discretizerFactory.getDiscretizer()
        discretizer.addShape(shape)
        discretizer.addEndpoints(lineStrings)
        discGeometry = discretizer.discretize(tolerance)
        topology = self._topologyFactory.getToplogy()
        return discGeometry.skeletonize(splitAtEndpoints=splitAtEndpoints,
                                        topology=topology)
