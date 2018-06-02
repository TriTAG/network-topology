"""Class to store and manipulate a mesh."""

from collections import defaultdict


class Mesh(object):
    """Class to store and manipulate a mesh."""

    def __init__(self, vertices, polygons, edge_nodes):
        """Initialize mesh object.

        Parameters
        ----------
        vertices : sequence
            A sequence of coordinate sequences
        polygons : sequence
            A sequence of vertex index sequences
        edge_nodes:
        """
        self._vertices = vertices
        self._polygons = polygons
        self._edge_nodes = edge_nodes

    def isInternal(self, nodeId):
        """Return true if the given vertex index is internal to the shape."""
        return not self._edge_nodes[nodeId]

    def polygons(self):
        """Return an iterator of polygon vertex lists."""
        return iter(self._polygons)

    def getVertex(self, nodeId):
        """Return coordinates of the given vertex."""
        return self._vertices[nodeId]

    def mergePolygons(self, polyIds):
        """Combine adjacent polygons into a single one.

        Parameters
        ----------
        polyIds : sequence
            A sequence of index values of adjacent polygons
        """
        edges = defaultdict(list)
        for poly in polyIds:
            nodes = self._polygons[poly]
            for n1, n2 in zip(nodes[:], nodes[1:] + nodes[:1]):
                n1, n2 = sorted([n1, n2])
                edges[n1, n2].append(poly)
        neighbours = defaultdict(list)
        for (n1, n2), polys in edges.items():
            if len(polys) == 1:
                neighbours[n1].append(n2)
                neighbours[n2].append(n1)
        current = neighbours.keys()[0]
        nodes = [current]
        while neighbours[current]:
            for neighbour in neighbours[current]:
                neighbours[current].remove(neighbour)
                if neighbour not in nodes:
                    nodes.append(neighbour)
                    current = neighbour
        self._polygons[polyIds[0]] = nodes
        for poly in polyIds[1:]:
            self._polygons[poly] = []
