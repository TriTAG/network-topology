"""Module for building meshes out of shapes."""
import random
import networkx as nx
from collections import defaultdict
from mesh import Mesh
from network_topology.skeletonizer.discrete.abstract import AbsDiscretizer
from edgeiterator import EdgeIterator
from shapely.geometry import Point, Polygon
from triangle import triangulate

__all__ = ['Mesher']


class Mesher(AbsDiscretizer):
    """Class to build meshes."""

    def __init__(self):
        """Constructor for MeshBuilder."""
        # self._logger = logging.getLogger('network-topology')
        self._vertices = []
        self._segments = []
        self._holes = []
        super(Mesher, self).__init__()

    def addShape(self, shape):
        """Add a shape to include in the mesh."""
        if shape.geom_type == 'MultiPolygon':
            for geom in shape.geoms:
                self.addShape(geom)
        else:
            self._addRing(shape.exterior)
            for ring in shape.interiors:
                self._addHole(ring)

    def addEndpoints(self, lineStrings):
        """Add endpoints of the linestrings to seed the mesh."""
        for ls in lineStrings:
            for i in [0, -1]:
                coords = list(ls.coords[i])
                if coords not in self._vertices:
                    self._vertices.append(coords)

    def _addRing(self, ring):
        lastIndex = len(self._vertices)
        self._vertices.append(list(ring.coords[0]))
        for x, y in ring.coords[1:]:
            if [x, y] in self._vertices:
                currentIndex = self._vertices.index([x, y])
            else:
                currentIndex = len(self._vertices)
                self._vertices.append([x, y])
            self._segments.append([lastIndex, currentIndex])
            lastIndex = currentIndex

    def _addHole(self, ring):
        self._addRing(ring)
        x, y = 0, 0
        minx, miny, maxx, maxy = ring.bounds
        while not Polygon(ring).contains(Point(x, y)):
            x = random.uniform(minx, maxx)
            y = random.uniform(miny, maxy)
        self._holes.append([x, y])

    def discretize(self, tolerance):
        """Construct and return a Mesh from the given geometry."""
        tri = {'vertices': self._vertices,
               'segments': self._segments,
               'holes': self._holes}
        tri = triangulate(tri, 'pq0Da{}i'.format(tolerance**2.0))
        graph = self._buildGraph(tri['triangles'])
        mesh = Mesh(tri['vertices'], tri['vertex_markers'],
                    graph)
        return mesh

    def _buildGraph(self, polygons):
        """Populate a graph for the given sequence of polygon nodes."""
        graph = nx.Graph()
        edges = defaultdict(list)
        for poly, nodes in enumerate(polygons):
            self._addPolygonToGraph(graph, edges, poly, nodes)
        return graph

    def _addPolygonToGraph(self, graph, edges, index, nodes):
        """Add a polygon to the graph."""
        graph.add_node(index, vertices=nodes)
        for edge in EdgeIterator(nodes):
            for other in edges[edge]:
                graph.add_edge(index, other, common=edge)
            edges[edge].append(index)
