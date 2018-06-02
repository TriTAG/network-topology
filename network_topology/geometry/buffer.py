"""Class to create buffers around an iterator of linestrings."""


from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import cascaded_union
import logging


class BufferMaker(object):
    """Class to create buffers around an iterator of linestrings."""

    def __init__(self):
        """Initialize BufferMaker."""
        self._logger = logging.getLogger('network-topology')

    def makeBufferedShape(self, lineStrings, thickness=14.0,
                          minInnerPerimeter=200):
        """Generate a buffered shape around the linestrings.

        Parameters
        ----------
        lineStrings : sequence
            A sequence of Shapely LineString objects
        thickness : float
            Thickness of the resulting shape. Corresponds to twice the
            thickness of the buffer
        minInnerPerimeter : float
            Interior shapes with perimeters smaller than this value will be
            removed
        """
        self._logger.info('Creating buffered shape')
        bufferedShapes = self._bufferShapes(lineStrings, thickness)
        bigShape = cascaded_union(bufferedShapes)
        filledShape = self._removeHoles(bigShape, minInnerPerimeter)
        bs = filledShape.simplify(thickness/10.0)
        self._logger.info('Completed buffered shape')
        return bs

    def _bufferShapes(self, lineStrings, thickness):
        bufferedShapes = []
        buf = thickness / 2.0
        for ls in lineStrings:
            bufferedShapes.append(ls.buffer(buf, resolution=2, join_style=3))
        return bufferedShapes

    def _removeHoles(self, bigShape, minInnerPerimeter):
        if bigShape.geom_type == 'MultiPolygon':
            filledShape = MultiPolygon(
                [self._polygonWithoutHoles(g, minInnerPerimeter)
                 for g in bigShape.geoms])
        else:
            filledShape = self._polygonWithoutHoles(bigShape,
                                                    minInnerPerimeter)
        return filledShape

    def _polygonWithoutHoles(self, polygon, minInnerPerimeter):
        return Polygon(polygon.exterior.coords,
                       [ring.coords
                        for ring in polygon.interiors
                        if ring.length > minInnerPerimeter])
